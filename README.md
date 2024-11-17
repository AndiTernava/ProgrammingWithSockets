# Universiteti i Prishtinës 'Hasan Prishtina'
- Fakulteti i Inxhinierisë Elektrike dhe Kompjuterike<br>
- Departamenti: Inxhinieri Kompjuterike dhe Softuerike<br>

# TCP Socket Programming
Projekt nga lënda "Rrjeta Kompjuterike".

# Contributors
- Alisa Shala
- Admir Rama
- Andi Tërnava

# Asistenti i lëndës
Mërgim Hoti


<h1>Kërkesat</h1>
<h3>Serveri</h3>
1. Të vendosen variabla te cilat përmbajnë numrin e portit (numri i portit të jetë i
çfarëdoshëm) dhe IP adresën (reale);<br>
2. Të jetë në gjendje të dëgjojë (listen) të paktën të gjithë anëtaret e grupit;<br>
3. Të pranojë kërkesat e pajisjeve që dërgojnë request (ku secili anëtarë i grupit duhet te e ekzekutoje të paktën një kërkesë në server);<br>
4. Të jetë në gjendje të lexoj mesazhet që dërgohen nga klientët;<br>
5. Të jetë në gjendje të jap qasje të plotë të paktën njërit klient për qasje ne folderat/përmbajtjen në file-t në server.<br>
<h3>Klienti</h3>
1. Të krijohet socket lidhja me server;<br>
2. Njeri nga pajisjet (klientët) të ketë privilegjet write(), read(), execute();<br>
3. Klientët tjerë të kenë vetëm read() permission;<br>
4. Të behet lidhja me serverin duke përcaktuar sakte portin dhe IP Adresën e serverit;<br>
5. Të definohen sakte socket e serverit dhe lidhje të mos dështojë;<br>
6. Të jetë në gjendje të lexojë përgjigjet që i kthehen nga serveri;<br>
7. Të dërgojë mesazh serverit si në formë tekstit;<br>
8. Të ketë qasje të plotë në folderat/ përmbajtjen në server.<br>


# Projekti i Dytë – Rrjetat Kompjuterike

Ky program implementon një sistem komunikimi mes një klienti dhe serveri duke përdorur protokollin e soketëve. Serveri pret lidhje nga klientët dhe ekzekuton komanda si `read`, `write`, `execute`, dhe `sudo` për të menaxhuar privilegjet e përdoruesve dhe për të manipuluar skedarët dhe përmbajtjen e serverit.

## Funksionalitetet e Serverit

1. **Konfigurimi i variablave**: Përcaktimi i numrit të portit dhe IP adresës së serverit.
2. **Dëgjimi për lidhje**: Serveri dëgjon kërkesat e klientëve dhe mund të pranojë lidhje nga të gjithë anëtarët e grupit.
3. **Pranimi i kërkesave**: Serveri pranon dhe përpunon kërkesat e dërguara nga klientët.
4. **Qasja në skedarë**: Serveri mund të ofrojë qasje të plotë në përmbajtjen e serverit për klientët që kanë privilegje të plota.

## Funksionalitetet e Klientit

1. **Krijimi i lidhjes**: Klienti krijon një lidhje me serverin.
2. **Privilegjet e përdoruesve**:
   - Njeri nga klientët ka privilegje për `write()`, `read()`, dhe `execute()`.
   - Klientët e tjerë kanë vetëm privilegje për `read()`.
3. **Dërgimi i mesazheve**: Klienti mund të dërgojë mesazhe te serveri.
4. **Leximi i përgjigjeve**: Klienti mund të lexojë përgjigjet që kthehen nga serveri.

## Mjedisi i Zhvillimit dhe Ekzekutimi i Projektit

Para se të startoni serverin dhe klientin, sigurohuni që keni aktivizuar mjedisin virtual në projektin tuaj.
- **Në Windows**:
  ```bash
  .\venv\Scripts\activate
Për të ekzekutuar projektin në **PyCharm** ose në **terminal**, ndiqni këto hapa:

### Hapat për Konfigurimin dhe Ekzekutimin në PyCharm:

1. **Instalimi i PyCharm**:
   - Sigurohuni që **PyCharm** është i instaluar në kompjuterin tuaj. Mund ta shkarkoni nga [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/).
     Para se të filloni, sigurohuni që keni instaluar të gjitha varësitë e nevojshme duke përdorur komandën:
     pip install -r requirements.txt
   
2. **Krijimi i Projektit në PyCharm**:
   - Hapni **PyCharm** dhe krijoni një projekt të ri Python.
   - Shtoni skedarët për serverin dhe klientin në direktorinë e projektit tuaj.
   - 
3. **Startoni Serverin**:
1. Ne dritaren e projektit,hapni skedarin server.py.
2. Sigurohuni që serveri ka variablat e nevojshme të vendosura (IP dhe porti).
3. Klikoni në butonin Run në PyCharm (ose përdorni shkurtesën Shift + F10) për të ekzekutuar skedarin server.py.(ose ne terminalin e pycharmit duke shenuar python server.py)
4. Serveri do të startohet dhe do të presë lidhje nga klientët.

  
4. **Startoni Klientin**:
1. Pas ekzekutimit të serverit, hapni një dritare tjetër në PyCharm për të ekzekutuar klientin.
2. Hapni skedarin client.py në këtë dritare.
3. Klikoni përsëri në butonin Run ose përdorni shkurtesën Shift + F10 për të startuar klientin.(ose ne terminalin e pycharmit duke shenuar python client.py)
4. Klienti do të lidhet me serverin, dhe mund të filloni të dërgoni komanda nga klienti tek serveri.
