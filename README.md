<h1>PërPërshkrimi i projektit të dytë – Rrjetat Kompjuterike</h1>
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
