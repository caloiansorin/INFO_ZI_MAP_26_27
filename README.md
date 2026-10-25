# Documentație tehnică – Aplicație Meteo

## 1. Titlul proiectului

**Aplicație Meteo – Interfață web pentru afișarea informațiilor meteorologice**

## 2. Descriere

Aplicația Meteo este o aplicație web care permite utilizatorului să introducă numele unui oraș și să vizualizeze informații despre starea vremii. Interfața este concepută pentru a afișa numele orașului, temperatura, condițiile meteorologice și viteza vântului.

Aplicația conține, de asemenea, un formular suplimentar prin care utilizatorul poate introduce o valoare personalizată. Interfața este realizată în HTML și CSS, iar datele meteorologice sunt furnizate de un backend dezvoltat în Python utilizând framework-ul FastAPI și afișate prin intermediul unor șabloane HTML dinamice.

## 3. Funcționalități

Aplicația include următoarele funcționalități:

1. Introducerea numelui unui oraș prin intermediul unui formular.
2. Trimiterea numelui orașului către ruta `/submit`, utilizând metoda HTTP POST.
3. Afișarea numelui orașului selectat.
4. Afișarea temperaturii și a descrierii condițiilor meteorologice.
5. Prezentarea vitezei vântului, exprimată în kilometri pe oră.
6. Afișarea unor elemente vizuale sugestive pentru vreme, precum simbolul meteorologic și pictograma vântului.
7. Introducerea și transmiterea unei valori suplimentare prin formularul asociat rutei `/ceva`.
8. Utilizarea unor variabile dinamice pentru afișarea datelor primite de la server.

## 4. Tehnologii

Proiectul utilizează următoarele tehnologii:

- **Python** – limbaj de programare utilizat pentru implementarea logicii aplicației, procesarea cererilor HTTP și integrarea cu servicii externe de furnizare a datelor meteorologice.
- **FastAPI** – framework web modern utilizat pentru dezvoltarea backend-ului și gestionarea endpoint-urilor aplicației.
- **HTML5** – pentru structurarea paginii web și definirea formularelor.
- **CSS3** – pentru stilizarea și organizarea aspectului vizual.
- **Jinja2** – motor de șabloane utilizat pentru afișarea dinamică a datelor furnizate de server.
- **HTTP/HTTPS** – protocol utilizat pentru comunicarea dintre client și server.

## 5. Arhitectură

Aplicația este implementată conform unei arhitecturi client-server bazate pe tehnologii web moderne. Componenta frontend realizează interacțiunea cu utilizatorul, iar backend-ul dezvoltat în Python FastAPI procesează cererile și furnizează datele necesare afișării informațiilor meteorologice.

### Componente principale

1. **Frontend (HTML/CSS)** – interfața utilizatorului și formularele de introducere a datelor.
2. **Backend FastAPI** – gestionează rutele aplicației (`/submit`, `/ceva`) și procesează cererile utilizatorului.
3. **Motor de șabloane Jinja2** – generează dinamic paginile HTML.
4. **Serviciu extern de date meteorologice** – furnizează informațiile meteorologice aplicației.
5. **Browser Client** – afișează rezultatele și permite interacțiunea cu aplicația.

### Schema arhitecturală

```text
┌───────────────────┐
│    Utilizator     │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Browser Client   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Frontend HTML/CSS │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Python + FastAPI  │
│      Backend      │
└──────┬─────┬──────┘
       │     │
       ▼     ▼
┌─────────┐ ┌──────────────┐
│ Jinja2  │ │ OpenWeather  │
│Template │ │     API      │
└─────────┘ └──────────────┘
```

### Flux operațional

1. Utilizatorul introduce numele unui oraș în interfața web.
2. Formularul transmite cererea către endpoint-ul FastAPI prin metoda HTTP POST.
3. Backend-ul procesează cererea și interoghează serviciul meteorologic extern.
4. Datele obținute sunt transmise către șablonul Jinja2.
5. Pagina HTML este generată dinamic și returnată browserului.
6. Utilizatorul vizualizează informațiile meteorologice actualizate.

Această arhitectură asigură separarea componentelor de prezentare, procesare și furnizare a datelor, facilitând mentenanța și dezvoltarea ulterioară a aplicației.

## 6. Instalare

Pentru rularea aplicației sunt necesare Visual Studio Code, Python și un browser web modern.

### Pași de instalare

1. Se descarcă sau se clonează proiectul.
2. Se deschide proiectul în Visual Studio Code.
3. Se instalează dependențele necesare:

```bash
pip install fastapi uvicorn jinja2
```

4. Se pornește serverul:

```bash
uvicorn main:app --reload
```

5. Aplicația poate fi accesată prin browser la adresa indicată de server.

## 7. Utilizare

1. Utilizatorul accesează aplicația prin intermediul browserului.
2. Introduce numele orașului pentru care dorește informații meteorologice.
3. Apasă butonul „Afișează starea vremii”.
4. Cererea este transmisă către ruta `/submit`.
5. Backend-ul procesează cererea și obține datele meteo.
6. Informațiile sunt afișate în interfață.
7. Formularul secundar permite transmiterea unei valori către ruta `/ceva`.

## 8. Testare

Testarea aplicației poate fi realizată prin verificarea interfeței, a formularelor și a comunicării cu serverul.

### Teste recomandate

1. Testarea interfeței grafice.
2. Testarea formularului pentru introducerea orașului.
3. Testarea formularului suplimentar.
4. Testarea câmpurilor obligatorii.
5. Testarea afișării dinamice a datelor.
6. Testarea compatibilității pe diferite dimensiuni ale ecranului.
7. Testarea endpoint-urilor FastAPI.
8. Testarea integrării cu API-ul meteorologic.

## 9. Limitări

1. Documentația prezintă arhitectura generală a aplicației, fără detalii complete privind implementarea backend-ului.
2. Nu sunt prezentate mecanisme de autentificare și autorizare.
3. Variabilele dinamice depind de datele furnizate de server.
4. Gestionarea erorilor poate fi îmbunătățită.
5. Funcționalitatea asociată rutei `/ceva` nu este descrisă în detaliu.
6. Structura CSS poate necesita optimizări pentru aplicații mai complexe.
7. Nu sunt implementate prognoze pe mai multe zile sau salvarea orașelor favorite.

## 10. Dezvoltări viitoare

1. Implementarea unei prognoze meteo extinse.
2. Afișarea umidității, presiunii atmosferice și temperaturii resimțite.
3. Îmbunătățirea validării datelor introduse.
4. Optimizarea interfeței pentru dispozitive mobile.
5. Adăugarea de teste automate pentru frontend și backend.
6. Salvarea istoricului căutărilor și a orașelor favorite.
7. Integrarea unor surse suplimentare de date meteorologice.

## 11. Autori

**Autor:** Veronica Ipati

## 12. Licență

Aplicația a fost dezvoltată în scop educațional, utilizând atât componente proprii, cât și servicii software furnizate de terți. Funcționalitatea sistemului se bazează pe integrarea tehnologiilor Python, FastAPI, Uvicorn, HTTPX și OpenWeatherMap.

Responsabilitatea pentru conținutul codului sursă și al documentației revine autorului proiectului. În cazul utilizării unor resurse externe, acestea trebuie menționate corespunzător și utilizate în conformitate cu termenii de utilizare impuși de furnizorii acestora.

Prezenta documentație reflectă versiunea actuală a aplicației și trebuie revizuită ori de câte ori sunt implementate modificări semnificative la nivelul funcționalităților sau arhitecturii sistemului.