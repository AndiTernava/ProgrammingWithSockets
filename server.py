import socket
import threading
import os
import subprocess
import queue
import keyboard
import time
from datetime import datetime, date
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Define server IP address, port, max clients, and timeout
SERVER_IP = '127.0.0.1'
PORT = 5557
MAX_CLIENTS = 1
TIMEOUT = 300
DATA_DIR = "Data"
CONNECTION_LOG = "connection_log.txt"
COMMAND_LOG = "command_log.txt"
PASSWORD = "root"

# Initialize data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    try:
        os.makedirs(DATA_DIR)
        print(f"Directory '{DATA_DIR}' created successfully.")
    except OSError as e:
        print(f"Error creating directory '{DATA_DIR}': {e}")

active_connections = 0
connection_lock = threading.Lock()
server_running = True
clients = []
waiting_queue = queue.Queue()


def check_shutdown():
    """Monitor for 'CTRL+C' to gracefully shutdown server."""
    global server_running
    while server_running:
        if keyboard.is_pressed('ctrl+c'):
            raise KeyboardInterrupt

        time.sleep(0.1)


def log_connection(message):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(Fore.CYAN + log_message + Style.RESET_ALL)  # Cyan for connection logs
        with open(CONNECTION_LOG, 'a') as log_file:
            log_file.write(log_message + "\n")
    except Exception as e:
        print(Fore.RED + f"Error logging connection: {e}" + Style.RESET_ALL)


def log_command(client_type, addr, command):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {client_type} client at {addr} issued command: {command}"
        print(Fore.YELLOW + log_message + Style.RESET_ALL)  # Yellow for command logs
        with open(COMMAND_LOG, 'a') as log_file:
            log_file.write(log_message + "\n")
    except Exception as e:
        print(Fore.RED + f"Error logging command: {e}" + Style.RESET_ALL)


def handle_client(conn, addr, client_type):
    global active_connections
    try:
        log_connection(f"[NEW CONNECTION] {addr} connected as {client_type}")

        conn.settimeout(TIMEOUT)

        while server_running:
            try:
                command = conn.recv(1024).decode('utf-8')
                if not command:
                    break

                log_command(client_type, addr, command)

                parts = command.split(" ", 2)
                if command.startswith("avelable"):
                    try:
                            files = os.listdir(DATA_DIR)
                            if files:
                                file_list = "\n".join(files)
                                conn.sendall(f"Available files:\n{file_list}".encode('utf-8'))
                            else:
                                conn.send("No files are available in the directory.".encode('utf-8'))
                    except Exception as e:
                            conn.send(f"Error listing files: {e}".encode('utf-8'))

                elif  command.startswith("read"):
                    # Read specific file
                    if len(parts) > 1:
                        file_name = parts[1]
                        # Ensure the filename ends with .txt
                        if not file_name.endswith(".txt"):
                            file_name += ".txt"

                        # Construct a safe path within DATA_DIR
                        safe_path = os.path.join(DATA_DIR, os.path.basename(file_name))
                        try:
                            if os.path.exists(safe_path):
                                with open(safe_path, 'r') as file:
                                    data = file.read()
                                conn.sendall(f"Content of {file_name}:\n\n{data}".encode('utf-8'))
                            else:
                                conn.send(f"Error: File {file_name} does not exist.".encode('utf-8'))
                        except Exception as e:
                            conn.send(f"Error reading file {file_name}: {e}".encode('utf-8'))
                    else:
                        try:
                            files = os.listdir(DATA_DIR)
                            if files:
                                file_list = "\n".join(files)
                                conn.sendall(f"Available files:\n{file_list}".encode('utf-8'))
                            else:
                                conn.send("No files are available in the directory.".encode('utf-8'))
                        except Exception as e:
                            conn.send(f"Error listing files: {e}".encode('utf-8'))

                elif  command.startswith("write") and len(parts) > 2 and client_type == "full_access":
                    # Write to specific file
                    file_name, new_data = parts[1], parts[2]
                    if not file_name.endswith(".txt"):
                            file_name += ".txt"

                    safe_path = os.path.join(DATA_DIR, os.path.basename(file_name))
                    try:
                        with open(safe_path, 'a') as file:
                            file.write(new_data + "\n")
                        conn.send(f"Data written to {file_name} successfully.".encode('utf-8'))
                    except Exception as e:
                        conn.send(f"Error writing to file {file_name}: {e}".encode('utf-8'))

                elif command.startswith("execute") and client_type == "full_access":
                    _, exec_command = command.split(" ", 1)
                    try:
                        output = subprocess.check_output(exec_command, shell=True, text=True)
                        conn.send(f"Execution result:\n{output}".encode('utf-8'))
                    except subprocess.CalledProcessError as e:
                        conn.send(f"Command failed with error:\n{e.output}".encode('utf-8'))
                    except Exception as e:
                        conn.send(f"General error occurred during execution:\n{str(e)}".encode('utf-8'))

                elif command.startswith("sudo") and client_type == "read_only":
                    _, password = command.split(" ", 1)
                    if password == PASSWORD:
                        client_type = "full_access"
                        conn.send("Upgraded to full access.".encode('utf-8'))
                    else:
                        conn.send("Incorrect password.".encode('utf-8'))

                elif command == "unsudo" and client_type == "full_access":
                    client_type = "read_only"
                    conn.send("Reverted to read-only access.".encode('utf-8'))

                else:
                    conn.send("Invalid command or insufficient permissions.".encode('utf-8'))

            except socket.timeout:
                conn.send("Connection timed out due to inactivity.".encode('utf-8'))
            except Exception as e:
                conn.send(f"An unexpected error occurred: {e}".encode('utf-8'))
                break

    except Exception as e:
        print(Fore.RED + f"Error handling client {addr}: {e}" + Style.RESET_ALL)
    finally:
        log_connection(Fore.RED + f"[DISCONNECTED] {addr} disconnected.")

        with connection_lock:
            active_connections -= 1
            clients.remove(conn)

        if not waiting_queue.empty():
            next_conn, next_addr = waiting_queue.get()
            with connection_lock:
                active_connections += 1
                clients.append(next_conn)
            next_conn.send("Slot is now available. You are now connected.".encode('utf-8'))
            threading.Thread(target=handle_client, args=(next_conn, next_addr, "read_only")).start()

        conn.close()


def start_server():
    global active_connections, server_running
    print(Fore.RED + f"Press CTRL+C to shutdown the server" + Style.RESET_ALL)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((SERVER_IP, PORT))
        server.listen()
        print(Fore.GREEN + f"[LISTENING] Server is listening on {SERVER_IP}:{PORT}" + Style.RESET_ALL)

        # shutdown_thread = threading.Thread(target=check_shutdown)
        # shutdown_thread.daemon = True  # Daemonize so it exits with the program
        # shutdown_thread.start()

        while server_running:
            try:
                if active_connections < MAX_CLIENTS and not waiting_queue.empty():
                    next_conn, next_addr = waiting_queue.get()
                    with connection_lock:
                        active_connections += 1
                        clients.append(next_conn)
                    next_conn.send("Slot is now available. You are now connected.".encode('utf-8'))
                    threading.Thread(target=handle_client, args=(next_conn, next_addr, "read_only")).start()
                    continue

                # Handle KeyboardInterrupt here
                try:
                    conn, addr = server.accept()
                except KeyboardInterrupt:
                    print(Fore.RED + "[SERVER SHUTDOWN] Server has been closed." + Style.RESET_ALL)
                    server_running = False
                    break

                with connection_lock:
                    if active_connections >= MAX_CLIENTS:
                        log_connection(f"[SERVER FULL] {addr} added to the waiting queue.")
                        waiting_queue.put((conn, addr))
                        conn.send("Server is full. You have been added to the waiting queue.".encode('utf-8'))
                        continue

                    active_connections += 1
                    clients.append(conn)

                client_type = "read_only"
                conn.send(f"Connected as {client_type} client.".encode('utf-8'))

                thread = threading.Thread(target=handle_client, args=(conn, addr, client_type))
                thread.start()
                log_connection(Fore.MAGENTA + f"[ACTIVE CONNECTIONS] {active_connections}" + Style.RESET_ALL)

            except Exception as e:
                print(Fore.RED + f"Error accepting connection: {e}" + Style.RESET_ALL)
                break


    except Exception as e:
        print(Fore.RED + f"Error starting server: {e}" + Style.RESET_ALL)

    finally:
        for client in clients:
            try:
                client.send("Server is shutting down.".encode('utf-8'))
                client.close()
            except Exception as e:
                print(Fore.RED + f"Error closing client connection: {e}" + Style.RESET_ALL)

        server.close()
        log_connection("[SERVER SHUTDOWN] Server has been closed.")


start_server()
