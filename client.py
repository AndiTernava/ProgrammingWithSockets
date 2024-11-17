import socket
import time
from colorama import init, Fore, Style

# Initialize colorama for cross-platform support
init(autoreset=True)

# Define server IP and port
SERVER_IP = '127.0.0.1'
PORT = 5557

# Color definitions for colored text output using colorama
COLOR_READ_ONLY = Fore.CYAN    # Cyan for read-only
COLOR_FULL_ACCESS = Fore.RED   # Red for full access
COLOR_PROMPT = Fore.GREEN      # Green for prompts
COLOR_RESPONSE = Fore.YELLOW   # Yellow for server responses
COLOR_ERROR = Fore.RED         # Red for error messages

# Function to handle socket-related exceptions
def handle_socket_error(error_message):
    print(f"{COLOR_ERROR}Error: {error_message}")
    client_socket.close()

# Function to attempt reconnecting to the server


# Connect to the server (with retry logic)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def reconnect_to_server():
    global client_socket  # Ensure we're working with the global client_socket variable
    while True:
        try:
            # Recreate the socket if the previous one was closed
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, PORT))
            print(f"{COLOR_PROMPT}Reconnected to the server.")
            initial_msg = client_socket.recv(1024).decode('utf-8')
            print(f"{COLOR_RESPONSE}{initial_msg}")
            if "added to the waiting queue" in initial_msg:
                print(f"{COLOR_PROMPT}Waiting for an available slot...")
                while True:
                    try:
                        # Wait for server to notify when slot becomes available
                        queue_msg = client_socket.recv(1024).decode('utf-8')
                        print(f"{COLOR_RESPONSE}{queue_msg}")
                        if "Slot is now available" in queue_msg:
                            print(f"{COLOR_PROMPT}Connected to the server.")
                            break
                    except socket.error as e:
                        handle_socket_error(f"Error while waiting for slot: {e}")
                        reconnect_to_server()  # Retry if connection is lost

            
            break
        except socket.error as e:
            print(f"{COLOR_ERROR}Failed to reconnect: {e}")
            print(f"{COLOR_PROMPT}Retrying in 5 seconds...")
            time.sleep(5)
# Attempt to connect to the server
try:
    client_socket.connect((SERVER_IP, PORT))
except socket.error as e:
    handle_socket_error(f"Failed to connect to the server: {e}")
    reconnect_to_server()  # Retry if connection fails

# Client initial type as read_only
client_type = "read_only"

# Handle server's initial connection response
try:
    initial_msg = client_socket.recv(1024).decode('utf-8')
    print(f"{COLOR_RESPONSE}{initial_msg}")
except socket.error as e:
    handle_socket_error(f"Error receiving initial message from server: {e}")
    reconnect_to_server()  # Retry if message cannot be received

# Check if client is added to the waiting queue
if "added to the waiting queue" in initial_msg:
    print(f"{COLOR_PROMPT}Waiting for an available slot...")
    while True:
        try:
            # Wait for server to notify when slot becomes available
            queue_msg = client_socket.recv(1024).decode('utf-8')
            print(f"{COLOR_RESPONSE}{queue_msg}")
            if "Slot is now available" in queue_msg:
                print(f"{COLOR_PROMPT}Connected to the server.")
                break
        except socket.error as e:
            handle_socket_error(f"Error while waiting for slot: {e}")
            reconnect_to_server()  # Retry if connection is lost


# Main interaction loop with the server
try:
    while True:
        # Choose color based on client type
        if client_type == "read_only":
            prompt_color = COLOR_READ_ONLY
            prompt = "Enter command (avlable-to see avelable files to read from,read <file_name>, sudo  to upgrade, exit): "
        elif client_type == "full_access":
            prompt_color = COLOR_FULL_ACCESS
             prompt = "Enter command (avlable-to see avelable files to read from,read <file_name>, write <new_data>, execute <command>, unsudo to downgrade, exit): "

        # Get user input with the prompt color
        command = input(f"{prompt_color}{prompt}{Style.RESET_ALL}").strip()

        if command == "exit":
            break

        # If command is 'sudo', prompt for password
        if command.startswith("sudo") and client_type == "read_only":
            password = input(f"{COLOR_PROMPT}Please enter the full access password: ")
            command += f" {password}"

        # Send command to the server
        try:
            client_socket.send(command.encode('utf-8'))
        except socket.error as e:
            print(f"{COLOR_ERROR}Error sending command to server: {e}")
            reconnect_to_server()  # Retry if sending the command fails
            continue

        # Receive and process server response
        try:
            response = client_socket.recv(1024).decode('utf-8')
            print(f"{COLOR_RESPONSE}{response}")
            if "Server is shutting down." in response:
                reconnect_to_server()
        except socket.error as e:
            print(f"{COLOR_ERROR}Error receiving server response: {e}")
            reconnect_to_server()  # Retry if receiving the response fails
            continue

        # Adjust client type based on server response
        if "Upgraded to full access" in response:
            client_type = "full_access"
        elif "Reverted to read-only access" in response:
            client_type = "read_only"

except KeyboardInterrupt:
    print(f"\n{COLOR_ERROR}Client interrupted by user. Closing connection...")

finally:
    client_socket.close()
    print(f"{COLOR_PROMPT}Connection closed.")
