
# Aplicație Meteo

**Documentație tehnică — Aplicație web pentru consultarea condițiilor meteorologice**

---

## Cuprins

1. [Introducere](#1-introducere)
2. [Obiectivele proiectului](#2-obiectivele-proiectului)
3. [Funcționalități](#3-funcționalități)
4. [Tehnologii utilizate](#4-tehnologii-utilizate)
5. [Arhitectura aplicației](#5-arhitectura-aplicației)
6. [Structura proiectului](#6-structura-proiectului)
7. [Instalare și configurare](#7-instalare-și-configurare)
8. [Mod de utilizare](#8-mod-de-utilizare)
9. [Testare și validare](#9-testare-și-validare)
10. [Limitări cunoscute](#10-limitări-cunoscute)
11. [Direcții de dezvoltare ulterioară](#11-direcții-de-dezvoltare-ulterioară)
12. [Autori](#12-autori)
13. [Licență](#13-licență)

---

## 1. Introducere

Aplicația Meteo este o aplicație web dezvoltată pentru consultarea informațiilor meteorologice corespunzătoare unui oraș selectat de utilizator. Aceasta utilizează o arhitectură de tip client–server, în care interfața web permite introducerea datelor, iar componenta backend gestionează solicitările și prelucrarea informațiilor meteorologice.

Datele sunt obținute prin intermediul serviciului extern **OpenWeatherMap**, folosind servicii API pentru identificarea coordonatelor geografice și preluarea condițiilor meteorologice.

Aplicația afișează următoarele informații:

- Numele orașului selectat.
- Temperatura curentă, exprimată în grade Celsius.
- Descrierea condițiilor meteorologice în limba română.
- Viteza vântului.

Interfața este realizată utilizând HTML5 și CSS3, iar logica aplicației este implementată în Python, cu ajutorul framework-ului FastAPI. Pentru afișarea dinamică a informațiilor este utilizat motorul de șabloane Jinja2.

În mod implicit, aplicația utilizează orașul Iași atunci când nu este specificat un alt nume de oraș.

## 2. Obiectivele proiectului

Obiectivul principal al proiectului constă în dezvoltarea unei aplicații web intuitive, care să faciliteze accesul la informații meteorologice prin integrarea unui serviciu extern.

Obiectivele specifice sunt:

- Dezvoltarea unei interfețe grafice pentru introducerea numelui unui oraș.
- Implementarea rutelor HTTP pentru gestionarea solicitărilor utilizatorului.
- Integrarea serviciilor API de geocodare și de preluare a datelor meteorologice.
- Procesarea și transmiterea datelor către interfața web.
- Utilizarea șabloanelor dinamice pentru afișarea rezultatelor.
- Documentarea procesului de instalare, configurare și utilizare.

## 3. Funcționalități

| Funcționalitate | Descriere |
|---|---|
| Căutarea după oraș | Permite introducerea numelui unui oraș printr-un formular HTML. |
| Afișarea temperaturii | Prezintă temperatura curentă în grade Celsius. |
| Descrierea vremii | Afișează condițiile meteorologice în limba română. |
| Viteza vântului | Prezintă valoarea vitezei vântului; unitatea trebuie verificată în implementare. |
| Geocodare | Determină latitudinea și longitudinea orașului. |
| Interfață grafică | Prezintă informațiile într-un card cu fundal deschis și colțuri rotunjite. |
| Oraș implicit | Utilizează Iași atunci când nu este specificat un alt oraș. |

Formularul transmite numele orașului printr-o solicitare HTTP de tip `POST`. Ulterior, utilizatorul este redirecționat către pagina principală, unde orașul este transmis prin parametrul URL `oras`.

## 4. Tehnologii utilizate

| Tehnologie | Rol |
|---|---|
| Python | Implementarea logicii aplicației. |
| FastAPI | Gestionarea rutelor și a solicitărilor HTTP. |
| HTML5 | Structurarea paginii web. |
| CSS3 | Stilizarea interfeței grafice. |
| Jinja2 | Generarea dinamică a paginilor HTML. |
| Requests | Efectuarea cererilor HTTP. |
| python-dotenv | Încărcarea variabilelor de mediu. |
| python-multipart | Procesarea formularelor. |
| Uvicorn | Pornirea serverului ASGI. |
| OpenWeatherMap API | Furnizarea datelor geografice și meteorologice. |

## 5. Arhitectura aplicației

Aplicația utilizează o arhitectură de tip client–server, formată din componenta frontend și componenta backend.

### 5.1. Componenta frontend

Interfața este definită în fișierul `index.html`, care conține formularele și elementele destinate afișării rezultatelor.

Stilizarea este realizată prin reguli CSS incluse în documentul HTML, în secțiunea `<style>` și, după caz, prin atributele `style`.

Pentru afișarea dinamică sunt utilizate variabile Jinja2:

- `{{ oras }}` — numele orașului.
- `{{ temperatura }}` — temperatura curentă.
- `{{ vreme }}` — descrierea vremii.
- `{{ viteza_vant }}` — viteza vântului.

### 5.2. Componenta backend

Logica principală este implementată în fișierul `main.py`, folosind FastAPI.

| Rută | Metodă | Responsabilitate |
|---|---|---|
| `/` | `GET` | Obține informațiile meteorologice și generează pagina HTML. |
| `/submit` | `POST` | Primește numele orașului și redirecționează utilizatorul către pagina principală. |

Funcția `raspuns_geocoding()` interoghează serviciul de geocodare pentru a obține coordonatele geografice ale orașului.

Funcția `afisare_vreme()` utilizează coordonatele obținute pentru a solicita date meteorologice și pentru a extrage temperatura, descrierea vremii și viteza vântului.

### 5.3. Fluxul de funcționare

1. Utilizatorul accesează pagina principală.
2. Introduce numele orașului în formular.
3. Formularul transmite datele către ruta `/submit`.
4. Serverul redirecționează utilizatorul către ruta `/`, transmițând orașul prin parametrul URL `oras`.
5. Aplicația solicită coordonatele geografice.
6. Backend-ul solicită datele meteorologice.
7. Informațiile sunt transmise șablonului HTML prin Jinja2.
8. Browserul afișează rezultatele.

## 6. Structura proiectului

```text
aplicatie-meteo/
├── main.py
├── README.md
├── .env
├── .gitignore
└── items/
    └── index.html
```

- `main.py` — logica backend și rutele FastAPI.
- `README.md` — documentația tehnică.
- `.env` — variabilele de configurare și cheia API.
- `.gitignore` — fișierele excluse din depozitul de cod.
- `items/index.html` — șablonul HTML.

Directorul `items` este utilizat pentru șabloane, conform configurării `Jinja2Templates(directory="items")`.

## 7. Instalare și configurare

### 7.1. Cerințe preliminare

Pentru rularea aplicației sunt necesare:

- Python.
- Acces la internet.
- O cheie API OpenWeatherMap.
- Un terminal sau un mediu de dezvoltare compatibil.

### 7.2. Crearea mediului virtual

Crearea mediului virtual:

```bash
python -m venv venv
```

Activarea în Windows:

```powershell
venv\Scripts\activate
```

Activarea în Linux sau macOS:

```bash
source venv/bin/activate
```

### 7.3. Instalarea dependențelor

```bash
pip install fastapi uvicorn jinja2 python-multipart requests python-dotenv
```

Pachetul `python-multipart` este necesar pentru procesarea formularelor trimise prin `Form()` în FastAPI.

### 7.4. Configurarea cheii API

În directorul principal se creează fișierul `.env`:

```dotenv
API_KEY=cheia_api_openweathermap
```

Valoarea trebuie înlocuită cu o cheie API validă.

**Important:** fișierul `.env` nu trebuie publicat într-un depozit public, deoarece poate conține informații confidențiale.

Exemplu de fișier `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.py[cod]
```

Backend-ul trebuie să încarce variabilele de mediu și să citească valoarea `API_KEY`.

### 7.5. Pornirea aplicației

Din directorul proiectului se execută:

```bash
uvicorn main:app --reload
```

Parametrul `main:app` indică obiectul FastAPI `app` definit în fișierul `main.py`.

Opțiunea `--reload` permite repornirea automată a serverului în timpul dezvoltării.

Aplicația poate fi accesată la adresa:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

## 8. Mod de utilizare

1. Se configurează cheia API și se pornește serverul.
2. Se accesează aplicația în browser.
3. Se introduce numele orașului dorit.
4. Se apasă butonul „Afișează starea vremii”.
5. Aplicația solicită informațiile de la OpenWeatherMap.
6. Rezultatele sunt afișate în interfața web.

Dacă nu este introdus un alt oraș, aplicația utilizează implicit Iași.

## 9. Testare și validare

Testarea urmărește verificarea rutelor backend, a formularelor, a comunicării cu serviciile externe și a afișării rezultatelor.

Scenariile următoare reprezintă teste propuse, nu rezultate confirmate ale unor teste executate.

| Scenariu | Acțiune | Rezultat așteptat |
|---|---|---|
| Accesarea paginii | Se accesează ruta `/`. | Pagina este generată și afișată. |
| Oraș valid | Se introduce un oraș existent. | Sunt afișate datele meteorologice. |
| Oraș implicit | Se accesează pagina fără parametrul `oras`. | Aplicația utilizează Iași. |
| Formular gol | Se trimite formularul fără un nume de oraș. | Comportamentul este verificat și validat. |
| Oraș inexistent | Se introduce un nume invalid. | Este afișat un mesaj de eroare. |
| Cheie API invalidă | Se configurează o cheie nevalidă. | Eroarea este gestionată corespunzător. |
| Lipsa conexiunii | Se întrerupe accesul la internet. | Utilizatorul este informat că datele nu pot fi preluate. |
| Răspuns API incomplet | Serviciul returnează date incomplete. | Aplicația gestionează lipsa informațiilor. |

### 9.1. Testarea interfeței

Se verifică:

- Afișarea corectă a elementelor HTML.
- Funcționarea câmpurilor și a butoanelor.
- Lizibilitatea informațiilor.
- Adaptarea paginii la dimensiunile ferestrei browserului.
- Transmiterea corectă a valorilor către șabloanele Jinja2.

### 9.2. Testarea integrării

Se verifică funcționarea serviciului de geocodare, a serviciului meteorologic și transmiterea datelor către șablonul HTML.

Pentru creșterea fiabilității, se recomandă implementarea unor teste automate pentru rutele FastAPI și funcțiile de prelucrare a răspunsurilor API.

## 10. Limitări cunoscute

Versiunea documentată prezintă următoarele limitări:

- Dependența de conexiunea la internet și de disponibilitatea serviciilor OpenWeatherMap.
- Necesitatea unei chei API valide.
- Tratarea incompletă a erorilor asociate orașelor inexistente și răspunsurilor API invalide.
- Lipsa limitelor de timp și a unei strategii de reîncercare pentru cererile HTTP.
- Utilizarea cererilor sincrone prin biblioteca `requests`.
- Lipsa unui mecanism de cache.
- Utilizarea unei pictograme meteo fixe.
- Posibila neconcordanță dintre unitatea reală a vitezei vântului și eticheta afișată în interfață.
- Lipsa testelor automate documentate.
- Neconectarea funcțională a formularului suplimentar la backend.

Viteza vântului trebuie verificată în implementare, deoarece API-ul meteorologic poate returna valoarea în metri pe secundă, în timp ce interfața este descrisă ca afișând km/h.

## 11. Direcții de dezvoltare ulterioară

Dezvoltarea ulterioară poate include:

1. Tratarea completă a erorilor și afișarea mesajelor corespunzătoare.
2. Validarea datelor introduse de utilizator.
3. Conversia vitezei vântului din m/s în km/h.
4. Adaptarea pictogramelor la condițiile meteorologice.
5. Adăugarea unei prognoze pentru următoarele zile.
6. Afișarea umidității, presiunii atmosferice și temperaturii resimțite.
7. Optimizarea interfeței pentru dispozitive mobile.
8. Separarea codului CSS în fișiere dedicate.
9. Implementarea testelor automate.
10. Introducerea unui mecanism de cache.
11. Evaluarea utilizării unui client HTTP asincron.
12. Configurarea limitelor de timp pentru solicitările externe.
13. Finalizarea funcționalităților asociate formularelor suplimentare.
14. Publicarea aplicației pe o platformă de găzduire.

## 12. Autori

- **Autor / autori:** [Numele autorului sau al membrilor echipei]
- **Instituție:** [Denumirea instituției, dacă este cazul]
- **Data realizării:** [Data realizării proiectului]

## 13. Licență

Licența proiectului nu este specificată în versiunea documentată.

Pentru distribuirea publică a aplicației, se recomandă alegerea unei licențe software adecvate, precum MIT, în funcție de intențiile autorului și de compatibilitatea cu licențele componentelor utilizate.

Utilizarea serviciilor OpenWeatherMap trebuie să respecte termenii și condițiile furnizorului, inclusiv condițiile asociate planului API utilizat.

Până la alegerea explicită a unei licențe, drepturile asupra codului original rămân supuse legislației aplicabile privind drepturile de autor.
