# Aplicatie Meteo - INFO ZI MAP 26-27

## 1. Titlul proiectului

**SimpleWeatherApp**

Accesul rapid la prognoze meteorologice precise joacă un rol esențial în planificarea activităților cotidiene și în adoptarea unor măsuri preventive împotriva fenomenelor climatice nefavorabile. Prezenta lucrare descrie proiectarea și implementarea aplicației „Simple Weather App”, o platformă web concepută pe principii de uzabilitate și simplitate vizuală, orientată spre interogarea eficientă a stării vremii pentru orice localitate.
Din punct de vedere arhitectural, soluția adoptă un model client-server decuplat. Modulul de backend este dezvoltat în Python, utilizând framework-ul FastAPI; acesta acționează ca un intermediar securizat între utilizator și serviciul extern OpenWeatherMap, preluând parametrii de căutare, procesând datele preluate prin interfața REST și furnizând răspunsurile în format JSON. În scopul asigurării securității aplicației, cheia API este izolată într-un fișier dedicat de configurare, prevenind expunerea acesteia pe partea de client. Interfața utilizator (frontend-ul) este construită dinamic cu ajutorul tehnologiilor standard HTML, CSS și JavaScript nativ, actualizând indicatorii meteorologici principali (temperatură, umiditate, viteza vântului) în mod asincron, fără reîncărcarea paginii. Totodată, sistemul include un mecanism coerent de interceptare și afișare a erorilor.
Rezultatul obținut este o platformă stabilă, ergonomică și scalabilă, ce creează premisele integrării unor funcționalități avansate, precum avertizările de vreme severă în timp real, hărțile radar interactive sau profilurile personalizate de utilizator.
Cuvinte-cheie: prognoză meteo, arhitectură client-server, integrare API, FastAPI, Python, dezvoltare web, JavaScript asincron.

## 2. Descriere

### 2.1 Contextul proiectului

Informatiile meteorologice sunt folosite frecvent pentru planificarea activitatilor zilnice, deplasari, activitati sportive si organizarea muncii. Desi datele sunt disponibile prin numeroase servicii online, utilizatorul trebuie de multe ori sa parcurga interfete incarcate, reclame sau informatii care nu sunt relevante pentru o verificare rapida. Aplicatia propusa raspunde acestei nevoi printr-o interfata concentrata pe un singur flux: introducerea unei localitati si afisarea conditiilor meteorologice curente.

Proiectul este o aplicatie web full-stack de dimensiune redusa. Browserul reprezinta componenta de prezentare, serverul FastAPI reprezinta componenta de control si integrare, iar OpenWeatherMap reprezinta sursa externa a datelor. Aceasta separare permite pastrarea cheii API pe server si ofera frontend-ului un raspuns simplificat, potrivit pentru interfata.

### 2.2 Scopul aplicatiei

Scopul principal este furnizarea rapida si lizibila a urmatoarelor informatii:

- numele localitatii pentru care a fost obtinuta informatia;
- temperatura curenta, exprimata in grade Celsius;
- descrierea starii vremii, furnizata in limba romana;
- viteza vantului, convertita in kilometri pe ora;
- pictograma meteorologica asociata starii vremii.

Aplicatia trebuie sa permita utilizatorului sa obtina informatia fara reincarcarea manuala a paginii. La prima accesare, frontend-ul solicita datele pentru localitatea configurata implicit in backend. Ulterior, formularul transmite numele introdus, iar cardul meteo este actualizat dinamic.

### 2.3 Obiective tehnice

Obiectivele proiectului sunt:

1. realizarea unui backend simplu, asincron si usor de pornit local;
2. integrarea cu un serviciu extern printr-o cerere HTTP controlata;
3. ascunderea cheii API fata de codul care ruleaza in browser;
4. separarea datelor externe de modelul de date prezentat utilizatorului;
5. tratarea explicita a erorilor de retea, timeout si localitate inexistenta;
6. crearea unei interfete responsive pentru desktop si dispozitive mobile;
7. documentarea instalarii, utilizarii si verificarii aplicatiei.

### 2.4 Domeniul de utilizare

Aplicatia este potrivita pentru demonstratii educationale, proiecte de laborator, exercitii de integrare a unui API extern si consultarea rapida a vremii. Nu este proiectata in versiunea actuala ca sistem meteorologic de precizie, platforma de prognoza profesionala sau serviciu critic. Datele afisate depind de acuratetea, acoperirea geografica si disponibilitatea OpenWeatherMap.

### 2.5 Rezumatul fluxului utilizatorului

Fluxul standard contine urmatoarele etape:

1. utilizatorul porneste serverul local;
2. browserul acceseaza ruta principala;
3. frontend-ul solicita ruta `/mesaj` fara parametru;
4. backend-ul foloseste localitatea implicita si interogheaza OpenWeatherMap;
5. serverul transforma raspunsul extern intr-un obiect compact;
6. browserul afiseaza rezultatul in cardul meteo;
7. utilizatorul cauta o alta localitate, daca este necesar;
8. frontend-ul reia periodic solicitarea pentru ultimul oras incarcat.

## 3. Functionalitati

### 3.1 Incarcarea vremii implicite

La evenimentul `DOMContentLoaded`, frontend-ul apeleaza functia `incarcaVreme()` fara argument. In acest caz este construit URL-ul `/mesaj`, iar backend-ul stabileste localitatea implicita. In implementarea actuala, valoarea este `Băicoi`, definita in `main.py` prin constanta `ORAS_IMPLICIT`.

Aceasta abordare evita duplicarea configurarii intre frontend si backend. Browserul nu trebuie sa cunoasca orasul implicit, iar schimbarea lui poate fi facuta pe server fara modificarea paginii HTML.

### 3.2 Cautarea unei localitati

Formularul contine un camp text si un buton de trimitere. Functia `cautaVreme()` elimina spatiile inutile de la inceputul si sfarsitul textului si porneste incarcarea numai daca exista o valoare. Numele localitatii este transmis ca parametru URL prin `encodeURIComponent`, pentru ca spatiile si caracterele speciale sa fie codificate corect.

Exemple de cautari valide sunt `Bucuresti`, `Cluj`, `Iasi`, `London` sau `Paris`. Interpretarea numelui este realizata de OpenWeatherMap, iar rezultatul final poate contine denumirea oficiala a localitatii identificata de serviciu.

### 3.3 Afisarea datelor

Dupa primirea unui raspuns JSON valid, frontend-ul actualizeaza urmatoarele elemente din DOM:

| Element         | Camp primit de la backend | Rol                                     |
| --------------- | ------------------------- | --------------------------------------- |
| numele orasului | `oras`                    | identifica localitatea gasita           |
| temperatura     | `temperatura`             | afiseaza valoarea in grade Celsius      |
| starea vremii   | `starea_vremii`           | afiseaza descrierea in limba romana     |
| viteza vantului | `viteza_vant`             | afiseaza viteza in km/h                 |
| imaginea        | `iconita`                 | construieste URL-ul pictogramei externe |

Imaginea este incarcata de la endpoint-ul de pictograme OpenWeatherMap folosind codul primit de la backend. Pictograma este ascunsa initial si devine vizibila dupa obtinerea unui raspuns valid.

### 3.4 Actualizarea automata

Dupa prima incarcare, frontend-ul porneste un timer cu `setInterval`. Intervalul este de zece minute, adica `10 * 60 * 1000` milisecunde. La fiecare executie, aplicatia verifica variabila `orasCurent`. Daca exista o localitate incarcata anterior, aceasta este transmisa din nou catre backend.

Actualizarea se face fara reincarcarea documentului HTML. Astfel, utilizatorul ramane pe aceeasi pagina, iar cardul este inlocuit cu valorile noi. In versiunea actuala intervalul este fix si nu exista un control in interfata pentru modificarea lui.

### 3.5 Tratarea erorilor

Frontend-ul verifica proprietatea `ok` a raspunsului HTTP. Pentru un raspuns care nu este in zona de succes, este generata o eroare si este afisat mesajul corespunzator. Erorile sunt prezentate in elementul `#eroare`, care este ascuns inaintea unei noi solicitari si afisat atunci cand operatia esueaza.

Backend-ul diferentiaza mai multe cazuri:

- codul `404` de la OpenWeatherMap devine raspuns HTTP `404` cu mesajul "Orașul nu a putut fi găsit.";
- o eroare de retea sau un timeout devine raspuns `504`;
- orice alt raspuns extern diferit de `200` devine raspuns `502`;
- o solicitare reusita produce un obiect JSON cu valorile necesare interfetei.

### 3.6 Responsive design

CSS-ul foloseste dimensiuni maxime si latimi responsive pentru formular si card. `max-width: 100%` permite incadrarea elementelor pe ecrane inguste, iar spatierea interna pastreaza lizibilitatea. Interfata foloseste un card central, o ierarhie vizuala clara si un camp de cautare amplasat deasupra rezultatului.

### 3.7 Functionalitati care nu sunt incluse

Pentru delimitarea corecta a domeniului, urmatoarele elemente nu fac parte din versiunea curenta:

- prognoza pe ore sau pe mai multe zile;
- autentificare si conturi personale;
- salvarea oraselor favorite;
- istoric persistent al cautarilor;
- harta, radar sau alerte meteorologice complexe;
- baza de date proprie;
- notificari push sau prin e-mail;
- detectarea automata a locatiei;
- panou de administrare si statistici de utilizare.

## 4. Tehnologii

### 4.1 Python

Python este limbajul folosit pentru server si permite implementarea rapida a unui serviciu web. Sintaxa compacta si ecosistemul disponibil il fac potrivit pentru un proiect educational in care accentul este pus pe integrarea unui API si pe intelegerea fluxului client-server.

### 4.2 FastAPI

FastAPI defineste obiectul aplicatiei, rutele HTTP si ciclul de viata al clientului HTTP. Ruta `/` returneaza fisierul HTML, iar ruta `/mesaj` realizeaza interogarea meteorologica. FastAPI genereaza automat documentatie OpenAPI, accesibila la `/docs` atunci cand serverul este pornit.

Aplicatia foloseste contextul `lifespan` pentru a crea un `httpx.AsyncClient` la pornire si pentru a-l inchide la oprire. Folosirea unui client reutilizabil evita crearea unui nou client pentru fiecare cerere si permite gestionarea ordonata a resurselor.

### 4.3 Uvicorn

Uvicorn este serverul ASGI care executa aplicatia FastAPI. Comanda `uvicorn main:app --reload` incarca obiectul `app` din modulul `main` si reporneste procesul de dezvoltare atunci cand fisierele sursa sunt modificate. Optiunea `--reload` este destinata dezvoltarii locale, nu unei configuratii de productie.

### 4.4 httpx

`httpx` este clientul HTTP asincron folosit pentru apelul catre OpenWeatherMap. In aplicatie este configurat un timeout de cinci secunde. Acest prag previne asteptarea nelimitata in cazul in care serviciul extern nu raspunde.

### 4.5 python-dotenv si variabilele de mediu

Modulul `python-dotenv` incarca fisierul `.env`, iar serverul citeste valoarea `API_KEY` prin `os.getenv`. Cheia nu este scrisa in `index.html` si nu este trimisa explicit de frontend. Aceasta separare reduce riscul expunerii accidentale a credidentialului in codul public al interfetei.

### 4.6 HTML5

HTML-ul defineste formularul de cautare, cardul meteo, elementul pentru pictograma, valorile textuale si containerul pentru mesajul de eroare. Atribute precum `lang="ro"`, `meta charset` si `viewport` contribuie la interpretarea corecta a paginii si la afisarea pe dispozitive mobile.

### 4.7 CSS3

CSS-ul defineste layout-ul central, fundalul, cardul meteo, campul de cautare, starile de focus si animatiile. Sunt folosite proprietati precum `flex`, `max-width`, `backdrop-filter`, `box-shadow` si `@keyframes`. Fontul este incarcat prin Google Fonts, cu o familie de rezerva in cazul in care resursa externa nu este disponibila.

### 4.8 JavaScript vanilla

JavaScript-ul realizeaza comunicarea cu backend-ul prin `fetch`, actualizeaza elementele DOM si gestioneaza timerul de actualizare. Alegerea JavaScript-ului fara framework reduce dependentele si este proportionala cu dimensiunea aplicatiei. Un framework ar deveni justificat daca ar fi adaugate mai multe ecrane, stare complexa, autentificare sau componente reutilizabile.

### 4.9 OpenWeatherMap

OpenWeatherMap furnizeaza datele meteo curente. Cererea foloseste parametrii `q` pentru localitate, `appid` pentru cheia API, `units=metric` pentru temperatura in sistem metric si `lang=ro` pentru descrierea in limba romana.

## 5. Arhitectura

### 5.1 Vedere de ansamblu

Aplicatia are trei zone functionale:

1. **prezentare**: pagina HTML, stilurile CSS si logica JavaScript;
2. **serviciu aplicativ**: FastAPI, rutele HTTP si transformarea raspunsului;
3. **integrare externa**: OpenWeatherMap si serviciul de pictograme.

```text
+------------------+       HTTP        +-----------------------+
| Browser          | ----------------> | FastAPI / Uvicorn    |
| HTML/CSS/JS      | <---------------- | GET /mesaj           |
+------------------+                   +-----------+-----------+
                                                   |
                                                   | HTTPS + API key
                                                   v
                                         +-----------------------+
                                         | OpenWeatherMap API    |
                                         +-----------------------+
```

### 5.2 Fluxul unei cautari

O cautare incepe cand utilizatorul trimite formularul. JavaScript-ul citeste valoarea campului si construieste un URL. Browserul trimite o cerere GET catre server. FastAPI primeste parametrul `oras`, adauga parametrii necesari pentru OpenWeatherMap si asteapta raspunsul asincron.

Dupa raspuns, serverul nu retransmite intregul obiect extern. Sunt extrase doar campurile relevante: `name`, `weather[0].description`, `weather[0].icon`, `main.temp` si `wind.speed`. Viteza vantului este convertita prin inmultirea valorii in metri pe secunda cu `3.6`. Rezultatul este rotunjit si transmis frontend-ului.

### 5.3 Fluxul unei incarcari initiale

La prima incarcare, URL-ul este `/mesaj`, fara parametrul `oras`. Valoarea implicita este rezolvata in semnatura functiei `mesaj`, unde parametrul are valoarea `ORAS_IMPLICIT`. Aceasta valoare este `Băicoi` in implementarea curenta.

Separarea aceasta este importanta: HTML-ul nu contine o localitate fixa, iar backend-ul ramane sursa unica pentru configurarea orasului implicit. Daca valoarea este modificata, nu este necesara editarea frontend-ului.

### 5.4 Ciclul de viata al clientului HTTP

Functia `lifespan` creeaza clientul asincron inainte ca aplicatia sa proceseze cereri. Clientul este pastrat in `app.state.client`, iar endpoint-ul il reutilizeaza prin `request.app.state.client`. La inchiderea aplicatiei, clientul este inchis cu `aclose()`.

Aceasta structura asigura eliberarea conexiunilor si evita mentinerea unor resurse deschise dupa oprirea serverului. Timeout-ul de cinci secunde este aplicat clientului si limiteaza durata asteptarii pentru serviciul extern.

### 5.5 Endpoint-uri

| Metoda | Ruta       | Parametri               | Rezultat                         |
| ------ | ---------- | ----------------------- | -------------------------------- |
| GET    | `/`        | niciunul                | pagina HTML principala           |
| GET    | `/mesaj`   | optional `oras`         | date meteo normalizate           |
| GET    | `/src/...` | calea fisierului static | fisier CSS sau alta resursa      |
| GET    | `/docs`    | niciunul                | documentatie interactiva FastAPI |

### 5.6 Contractul endpoint-ului `/mesaj`

Raspunsul de succes are forma:

```json
{
  "oras": "Cluj-Napoca",
  "starea_vremii": "Cer senin",
  "temperatura": 21,
  "viteza_vant": 12.6,
  "iconita": "01d"
}
```

Proprietatea `oras` este un text, `starea_vremii` este un text, `temperatura` este o valoare numerica rotunjita, `viteza_vant` este o valoare numerica exprimata in km/h, iar `iconita` este codul folosit pentru construirea imaginii meteo.

Un exemplu de eroare este:

```json
{
  "detail": "Orașul nu a putut fi găsit."
}
```

Frontend-ul afiseaza mesajul primit de server atunci cand raspunsul nu este de succes. Contractul este suficient de mic pentru interfata, dar poate fi extins ulterior cu umiditate, presiune, coordonate sau fus orar.

### 5.7 Organizarea proiectului

```text
INFO_ZI_MAP_26_27/
|-- main.py              # Serverul FastAPI si endpoint-urile
|-- requirements.txt     # Dependentele Python
|-- .env                 # Configurare locala, nu se publica
|-- .gitignore           # Fisiere excluse din versionare
|-- README.md            # Documentatia proiectului
`-- src/
    |-- index.html       # Interfata si logica JavaScript
    `-- index.css        # Stilurile vizuale
```

### 5.8 Responsabilitatea fisierelor

`main.py` gestioneaza configurarea, clientul extern, servirea paginii si ruta meteo. `index.html` contine structura interfetei si codul JavaScript al aplicatiei. `index.css` contine stilurile, animatiile si regulile responsive. `requirements.txt` descrie dependentele instalabile prin pip. Fisierul `.env` contine configurarea sensibila si trebuie pastrat local.

### 5.9 Decizii arhitecturale

A fost aleasa arhitectura client-server deoarece cheia API nu trebuie expusa in browser, iar backend-ul poate transforma raspunsul extern intr-un format stabil. A fost aleasa comunicarea REST prin GET deoarece interogarea este fara efecte secundare si poate fi reprezentata natural printr-un URL.

Clientul HTTP asincron permite procesarea eficienta a asteptarii catre un serviciu extern. In acelasi timp, aplicatia ramane usor de inteles deoarece nu foloseste o baza de date, un sistem de autentificare sau un mecanism de mesagerie.

## 6. Instalare

### 6.1 Cerinte hardware si software

Pentru utilizarea locala sunt suficiente un calculator obisnuit, aproximativ 100 MB pentru proiect si dependente, o conexiune la internet si un browser modern. Este necesara o versiune Python compatibila cu dependentele FastAPI si Uvicorn. Se recomanda Python 3.10 sau mai nou.

Sistemul poate fi Linux, macOS sau Windows. Comenzile pentru activarea mediului virtual difera in functie de sistem, dar fisierele proiectului si comanda de instalare raman aceleasi.

### 6.2 Obtinerea proiectului

Deschideti un terminal in directorul proiectului:

```bash
cd INFO_ZI_MAP_26_27
```

Daca proiectul a fost clonat intr-o alta locatie, folositi calea efectiva a directorului. Toate comenzile de mai jos trebuie executate din radacina care contine `main.py` si `requirements.txt`.

### 6.3 Crearea mediului virtual

```bash
python -m venv .venv
```

Mediul virtual izoleaza dependentele proiectului de instalarea globala Python. Aceasta izolare reduce conflictele dintre versiuni si permite stergerea sau reconstruirea mediului fara afectarea altor proiecte.

### 6.4 Activarea mediului virtual

Pe Linux si macOS:

```bash
source .venv/bin/activate
```

Pe Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Pe Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Dupa activare, promptul terminalului afiseaza de obicei numele `.venv`.

### 6.5 Instalarea dependentelor

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Fisierul de dependente contine `fastapi`, `uvicorn[standard]`, `httpx` si `python-dotenv`. Pachetele tranzitive sunt instalate automat de pip.

### 6.6 Configurarea cheii API

Creati un fisier numit `.env` in radacina proiectului:

```env
API_KEY=cheia_ta_openweathermap
```

Inlocuiti valoarea demonstrativa cu cheia obtinuta de la OpenWeatherMap. Nu adaugati ghilimele daca acestea nu sunt necesare si nu includeti cheia in `index.html`.

Verificati ca `.env` este exclus prin `.gitignore`. Cheia API trebuie tratata ca un secret: nu trebuie publicata in repository, introdusa in capturi de ecran sau transmisa altor persoane.

### 6.7 Pornirea aplicatiei

```bash
uvicorn main:app --reload
```

Serverul va afisa adresa locala, de obicei `http://127.0.0.1:8000`. Deschideti adresa in browser. Optiunea `--reload` reporneste serverul cand sunt detectate modificari in fisierele Python; ea este utila la dezvoltare.

### 6.8 Verificarea instalarii

Verificati pagina principala:

```bash
curl http://127.0.0.1:8000/
```

Verificati endpoint-ul meteo:

```bash
curl "http://127.0.0.1:8000/mesaj?oras=Bucuresti"
```

Accesati documentatia generata automat:

```text
http://127.0.0.1:8000/docs
```

Daca primul endpoint returneaza HTML, serverul este pornit. Daca al doilea returneaza JSON cu valorile asteptate, configurarea API este functionala.

### 6.9 Oprirea si repornirea

Pentru oprire, reveniti in terminalul in care ruleaza Uvicorn si apasati `Ctrl+C`. Pentru repornire, activati din nou mediul virtual daca este necesar si rulati aceeasi comanda. Mediul virtual nu trebuie recreat la fiecare pornire.

### 6.10 Probleme frecvente la instalare

Daca `python` nu este gasit, verificati instalarea Python sau folositi comanda disponibila in sistem, de exemplu `python3`. Daca activarea mediului este blocata in PowerShell, verificati politica locala de executare. Daca pip nu poate instala pachetele, verificati conexiunea la internet si versiunea Python.

Un raspuns `401` sau `403` de la serviciul extern indica de obicei o cheie invalida, lipsa activarii cheii sau o variabila `API_KEY` incarcata gresit. Un raspuns `404` pentru un oras indica faptul ca serviciul nu a identificat localitatea transmisa.

## 7. Utilizare

### 7.1 Deschiderea aplicatiei

Porniti serverul si deschideti `http://127.0.0.1:8000`. Pagina contine un camp de cautare si un card meteorologic. La inceput, campurile pot afisa valori de asteptare pana la primirea raspunsului.

### 7.2 Cautarea unui oras

Introduceti numele unei localitati in campul de cautare, apoi apasati **Cauta** sau tasta Enter. Folositi nume suficient de clare pentru a reduce ambiguitatea. Pentru localitati cu acelasi nume, includeti tara atunci cand API-ul permite acest format, de exemplu `Paris, FR`.

Dupa raspuns, cardul afiseaza numele returnat de OpenWeatherMap, nu neaparat forma exacta introdusa de utilizator. Aceasta este denumirea identificata de serviciul extern.

### 7.3 Interpretarea rezultatului

Temperatura este exprimata in grade Celsius deoarece backend-ul foloseste `units=metric`. Viteza vantului primita in metri pe secunda este inmultita cu `3.6`, apoi rotunjita la o zecimala. Descrierea vremii este solicitata cu `lang=ro`, iar pictograma este incarcata pe baza codului extern.

### 7.4 Actualizarea periodica

Dupa o cautare reusita, numele orasului returnat este memorat in `orasCurent`. La fiecare zece minute, browserul reia solicitarea pentru aceasta localitate. Daca pagina este inchisa, istoricul nu este pastrat, deoarece aplicatia nu foloseste local storage sau baza de date.

### 7.5 Comportamentul la eroare

Daca orasul nu poate fi gasit, cardul afiseaza un mesaj de eroare. Daca serviciul extern nu raspunde la timp, mesajul indica indisponibilitatea sau expirarea asteptarii. Utilizatorul poate incerca din nou dupa verificarea numelui localitatii, a conexiunii si a cheii API.

### 7.6 Scenariu de utilizare complet

Un scenariu tipic este urmatorul. Utilizatorul porneste serverul, deschide pagina si vede vremea pentru localitatea implicita. Introduce `Cluj`, apasa butonul de cautare si asteapta actualizarea cardului. Pagina afiseaza orasul identificat, temperatura, descrierea, pictograma si vantul. Dupa zece minute, browserul solicita din nou datele fara ca utilizatorul sa intervina.

### 7.7 Accesibilitate si experienta vizuala

Campul de cautare este focalizat automat la incarcarea paginii, iar butonul poate fi activat prin tastatura. Contrastul dintre text si fundal este sustinut de cardul deschis si textul inchis. Mesajul de eroare este separat vizual de continutul normal. Pentru o versiune viitoare pot fi adaugate descrieri mai precise pentru pictograme, stari de incarcare si suport extins pentru navigare cu tastatura.

## 8. Testare

### 8.1 Strategia de testare

Deoarece proiectul nu contine inca teste automate, verificarea se bazeaza pe teste manuale ale fluxului principal si pe apeluri directe catre endpoint-uri. Testarea trebuie facuta cu serverul pornit si cu un fisier `.env` valid. Rezultatele pot varia daca serviciul meteorologic extern este indisponibil.

### 8.2 Matrice de scenarii

| ID  | Scenariu           | Actiune                                   | Rezultat asteptat                             |
| --- | ------------------ | ----------------------------------------- | --------------------------------------------- |
| T01 | Incarcare initiala | Se acceseaza `/`                          | Se afiseaza pagina HTML                       |
| T02 | Oras implicit      | Se asteapta incarcarea paginii            | Se afiseaza vremea pentru orasul configurat   |
| T03 | Oras valid         | Se cauta `Bucuresti`                      | Cardul se actualizeaza cu date meteo          |
| T04 | Oras inexistent    | Se cauta un nume aleator                  | Se afiseaza mesajul de localitate inexistenta |
| T05 | Camp gol           | Se trimite formularul fara text           | Nu se face o cautare inutila                  |
| T06 | Caractere speciale | Se cauta un oras cu spatii sau diacritice | Parametrul este codificat corect              |
| T07 | Actualizare        | Se asteapta intervalul configurat         | Se reia cautarea ultimului oras               |
| T08 | Timeout            | Serviciul extern nu raspunde              | Se afiseaza eroare controlata                 |
| T09 | Cheie invalida     | Se modifica temporar `API_KEY`            | Backend-ul returneaza eroare externa          |
| T10 | Documentatie       | Se acceseaza `/docs`                      | Se incarca interfata OpenAPI                  |

### 8.3 Testarea endpoint-ului principal

```bash
curl -i http://127.0.0.1:8000/
```

Se verifica un cod de succes si continut HTML. Pagina trebuie sa contina formularul, elementul pentru cardul meteo si referinta catre `/src/index.css`.

### 8.4 Testarea endpoint-ului meteo

```bash
curl -i "http://127.0.0.1:8000/mesaj?oras=Cluj"
```

Un rezultat reusit trebuie sa contina cheile `oras`, `starea_vremii`, `temperatura`, `viteza_vant` si `iconita`. Valorile pot varia de la un moment la altul.

### 8.5 Testarea erorii 404

Folositi un nume care nu reprezinta o localitate reala:

```bash
curl -i "http://127.0.0.1:8000/mesaj?oras=LocalitateCareNuExista999"
```

Backend-ul trebuie sa intoarca un raspuns `404` si un camp `detail`. Frontend-ul transforma acest raspuns intr-un mesaj vizibil in card.

### 8.6 Testarea interfetei

Testati pagina in browser la o latime desktop si la o latime mobila. Verificati ca formularul nu depaseste ecranul, ca textul nu se suprapune si ca pictograma este vizibila dupa un raspuns valid. Verificati si trimiterea prin buton, precum si trimiterea prin Enter.

### 8.7 Testarea actualizarii periodice

Pentru testarea manuala completa este necesara asteptarea a zece minute. In timpul verificarii, pastrati pagina deschisa si observati in instrumentele browserului daca apare o noua cerere `/mesaj`. Intr-un mediu de dezvoltare, intervalul poate fi temporar redus, dar aceasta modificare nu trebuie confundata cu setarea finala documentata.

### 8.8 Testarea regresiei

Dupa modificarea backend-ului, repetati T01-T05. Dupa modificarea frontend-ului, repetati T02-T07. Dupa modificarea configurarii sau a dependentelor, repetati T01, T03 si T10. Scopul este sa fie verificat fluxul principal dupa fiecare schimbare.

### 8.9 Limitele testarii curente

Nu exista teste unitare pentru transformarea raspunsului, teste de integrare cu un serviciu mock, teste end-to-end automatizate sau pipeline CI/CD. Dependenta de un serviciu extern face ca unele rezultate sa fie nedeterministe. Aceste limitari trebuie rezolvate inaintea unei utilizari de productie.

## 9. Limitari

### 9.1 Dependenta de OpenWeatherMap

Aplicatia nu produce date meteorologice proprii. Daca OpenWeatherMap este indisponibil, lent sau limiteaza numarul de cereri, utilizatorul nu poate primi un rezultat. Calitatea informatiilor depinde de statiile si modelele folosite de furnizor.

### 9.2 Localitati ambigue

Cautarea prin nume poate produce mai multe rezultate posibile. In lipsa unor coordonate sau a unui cod de tara, serviciul extern poate alege o localitate diferita de cea intentionata. Versiunea actuala nu afiseaza coordonatele pentru confirmare.

### 9.3 Lipsa persistentei

Istoricul cautarilor si orasul ales nu sunt salvate. La inchiderea sau reincarcarea paginii este pornit din nou fluxul pentru orasul implicit. Nu exista profil de utilizator, favorite sau configurare persistenta.

### 9.4 Lipsa autentificarii si autorizarii

Orice persoana care poate accesa serverul poate folosi endpoint-ul. Pentru un serviciu public ar fi necesare autentificare, autorizare, limitarea traficului si reguli explicite CORS.

### 9.5 Gestionarea secretelor

Cheia este citita din `.env`, ceea ce este potrivit pentru dezvoltare locala. Pentru productie ar fi preferabil un secret manager, variabile de mediu administrate de platforma si rotirea periodica a cheii.

### 9.6 Observabilitate redusa

Aplicatia nu are logging structurat, monitorizare, metrici sau alerte. In cazul unei erori, utilizatorul vede un mesaj, dar administratorul nu dispune de un jurnal centralizat pentru diagnostic.

### 9.7 Lipsa unui nivel de productie

Serverul pornit cu `--reload` este destinat dezvoltarii. O implementare publica ar necesita un proces de deploy, HTTPS, proxy, configurarea CORS, politici de securitate, rate limiting si o strategie de actualizare.

### 9.8 Limitari ale interfetei

Interfata prezinta un singur rezultat si putine variabile. Nu exista grafice, prognoza, compararea oraselor, unitati configurabile sau un mod offline. Animatiile si fontul extern pot avea comportament diferit daca browserul nu suporta anumite proprietati sau daca resursele externe nu se incarca.

## 10. Dezvoltari viitoare

### 10.1 Extinderea datelor meteo

O versiune ulterioara poate include umiditate, presiune, vizibilitate, directia vantului, senzatie termica, rasarit si apus. Contractul `/mesaj` ar putea fi extins gradual, pastrand campurile actuale pentru compatibilitate.

### 10.2 Prognoza pe mai multe zile

Integrarea unui endpoint de prognoza ar permite afisarea evolutiei vremii pe cinci sau sapte zile. Datele ar putea fi reprezentate prin carduri sau grafice, cu accent pe compararea temperaturii minime si maxime si pe probabilitatea de precipitatii.

### 10.3 Geolocalizare si selectarea tarii

Browserul poate solicita permisiunea pentru geolocalizare, iar coordonatele ar putea fi trimise catre backend. Alternativ, formularul poate primi oras si cod de tara. Ambele abordari ar reduce ambiguitatea localitatilor.

### 10.4 Favorite si persistenta

Local storage ar putea retine ultimul oras sau o lista mica de favorite fara cont. Pentru mai multi utilizatori ar fi necesara o baza de date si un sistem de autentificare. Persistenta ar permite afisarea rapida a oraselor folosite frecvent.

### 10.5 Testare automata

Backend-ul poate primi teste unitare pentru conversia vitezei, tratarea statusurilor externe si construirea raspunsului. Testele de integrare pot folosi un client HTTP simulat, astfel incat rezultatul sa nu depinda de OpenWeatherMap. Pentru frontend pot fi introduse teste end-to-end care verifica formularul, afisarea si mesajele de eroare.

### 10.6 Calitatea codului si observabilitate

Pot fi adaugate linting, formatare automata, logging structurat, identificatori de corelare si metrici. Un pipeline CI ar putea instala dependentele, rula testele si verifica stilul la fiecare modificare.

### 10.7 Securitate si productie

Pentru un deploy public ar trebui folosite HTTPS, secret manager, rate limiting, reguli CORS restrictive, validarea lungimii parametrului `oras`, protectie impotriva abuzului si monitorizarea consumului API. Configurarea ar trebui separata pe medii: dezvoltare, testare si productie.

### 10.8 Containerizare si deploy

Un `Dockerfile` ar putea standardiza mediul de rulare, iar un serviciu de deploy ar putea porni aplicatia cu un server ASGI configurat pentru productie. Pentru disponibilitate mai mare ar putea fi adaugat un reverse proxy si un mecanism de restart.

### 10.9 Accesibilitate

Dezvoltarea viitoare ar trebui sa includa etichete mai descriptive, stari de incarcare, suport pentru cititoare de ecran, contrast verificat si navigare completa prin tastatura. Pictograma ar trebui sa aiba un text alternativ construit din descrierea vremii.

## 11. Autori

Proiectul a fost realizat de echipa **INFO ZI MAP 26-27**.

- Autor 1: de completat
- Autor 2: de completat
- Autor 3: de completat

Numele complete, rolurile si contributiile individuale trebuie completate inaintea predarii finale. O forma recomandata pentru completare este:

| Autor        | Rol                     | Contributie                               |
| ------------ | ----------------------- | ----------------------------------------- |
| Nume Prenume | dezvoltare backend      | FastAPI, integrare API, tratarea erorilor |
| Nume Prenume | dezvoltare frontend     | HTML, CSS, JavaScript, interfata          |
| Nume Prenume | documentatie si testare | scenarii, verificare, redactare           |

## 12. Licenta

Repository-ul nu contine in prezent un fisier `LICENSE` si nu declara o licenta open-source explicita. Pana la alegerea unei licente de catre autori, codul trebuie considerat material educational al proiectului si nu trebuie redistribuit sau reutilizat comercial fara acordul autorilor.

Daca autorii doresc publicarea proiectului, trebuie aleasa o licenta si adaugat fisierul oficial `LICENSE`. Licenta MIT este o optiune permisiva, dar alegerea trebuie facuta de titularii drepturilor. Dupa alegere, aceasta sectiune trebuie actualizata cu numele titularilor si anul aplicabil.

Documentatia descrie versiunea curenta a proiectului. Orice functie adaugata ulterior trebuie reflectata in sectiunile de functionalitati, arhitectura, instalare, testare, limitari si dezvoltari viitoare.
