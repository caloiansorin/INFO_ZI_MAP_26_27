# Documentatie tehnica
1. Titlul proiectului - aplicatie meteo

2. Descriere -
Acest proiect reprezintă o aplicație web ușoară și rapidă, concepută pentru a furniza date meteorologice în timp real pentru un anumit oraș. Scopul principal este eliminarea interfețelor supraîncărcate și a funcționalităților redundante întâlnite în soluțiile comerciale, oferind utilizatorului acces instantaneu la parametrii esențiali (temperatură, condiții atmosferice, vânt). Sistemul interoghează o sursă externă de date de înaltă precizie și randează informația direct pe server, asigurând un timp minim de încărcare.

3. Funcționalități -
Afișarea temperaturii curente, stării generale a vremii și vitezei vântului.

Motor de căutare integrat printr-un formular HTML, permițând interogarea vremii pentru orice oraș.

Interfață grafică responsivă și prietenoasă, dezvoltată direct cu CSS inline pentru o încărcare rapidă.

Redirecționare automată (PRG - Post/Redirect/Get) la trimiterea datelor, asigurând un URL curat cu parametri de interogare.

4. Tehnologii -
Backend: Python 3, FastAPI, Uvicorn (server ASGI).

Templating): Jinja2 (pentru injectarea datelor în pagina HTML).

Preluare Date: Biblioteca requests pentru apeluri HTTP către serviciile externe.

Frontend: HTML5 cu CSS inline.

API Extern: OpenWeatherMap API.

Securitate/Configurare: python-dotenv pentru gestionarea variabilelor de mediu și ascunderea cheii API.

5. Arhitectură -
Clientul (Browser-ul): Trimite o cerere HTTP GET către serverul FastAPI.

Backend-ul (FastAPI): Preia cererea și efectuează un apel API (REST) asincron către serverele OpenWeatherMap, transmițând cheia de autentificare și orașul dorit.

Procesarea datelor: Răspunsul JSON primit de la OpenWeather este parsat, extrăgându-se doar parametrii esențiali.

Generarea vizuală (Jinja2): Datele extrase sunt trimise către șablonul HTML (index.html).

Răspunsul: Serverul returnează clientului pagina HTML completă, inclusiv stilurile CSS inline, permițând afișarea instantanee.

6. Instalare -
Clonați repository-ul sau descărcați fișierele sursă:git clone <https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git>

Navigați în directorul proiectului.   
Creați și activați un mediu virtual Python:python -m venv venvsource venv/bin/activate (Linux/Mac) sau venv\Scripts\activate (Windows)Instalați dependențele necesare:pip install fastapi uvicorn requests jinja2Obțineți o cheie API de la OpenWeatherMap și configurați-o în fișierul main.py (ideal prin variabile de mediu).

7. Utilizare -
Pentru a porni serverul local de dezvoltare, rulați următoarea comandă în terminal:
uvicorn main:app --reload
Aplicația va fi accesibilă în browser la adresa de bază: [http://127.0.0.1:8000](http://127.0.0.1:8000)

8. Testare -
Testare funcțională: Verificarea rutelor în browser pentru a asigura afișarea corectă a paginii index și a datelor meteo.

Validarea API-ului extern: Monitorizarea răspunsurilor HTTP și simularea erorilor.

Testare vizuală: Verificarea modului în care regulile CSS inline se aplică pe diferite dimensiuni de ecran folosind uneltele de dezvoltator din browser.

9. Limitări -
Apelurile către OpenWeather sunt făcute sincron folosind biblioteca requests, ceea ce poate bloca procesele asincrone ale FastAPI în cazul unui număr mare de accesări simultane.

Lipsa unui sistem de tratare a excepțiilor (ex. try-except). Dacă se introduce un oraș invalid, indexarea listei de geocoding (raspuns_geocoding(oras)[0]) va genera o eroare de tip IndexError.

Utilizarea CSS-ului inline direct în tag-urile formularului face codul mai puțin curat și dificil de scalat pe viitor.

10. Dezvoltări viitoare -
Înlocuirea bibliotecii requests cu httpx (client HTTP asincron) pentru a optimiza performanța backend-ului.

Implementarea gestionării erorilor (Error Handling) pentru a afișa utilizatorului un mesaj prietenos atunci când orașul nu este găsit în baza de date.

Separarea codului de stilizare în fișiere .css externe și implementarea unui modul simplu de caching pentru a limita apelurile repetitive către API-ul extern.

11. Autori -
Benchea Amadeus

12. Licență -
Acest proiect este distribuit sub licența MIT, permițând utilizarea, modificarea și distribuirea liberă a codului sursă.