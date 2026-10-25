Documentație tehnică – Aplicație Meteo
1. Titlul proiectului

Aplicație Meteo – Interfață web pentru afișarea informațiilor meteorologice

2. Descriere

Aplicația Meteo este o aplicație web care permite utilizatorului să introducă numele unui oraș și să vizualizeze informații despre starea vremii. Interfața este concepută pentru a afișa numele orașului, temperatura, condițiile meteorologice și viteza vântului.

Aplicația conține, de asemenea, un formular suplimentar prin care utilizatorul poate introduce o valoare personalizată. Interfața este realizată în HTML și CSS, iar datele meteorologice sunt furnizate de un backend dezvoltat în Python utilizând framework-ul FastAPI și afișate prin intermediul unor șabloane HTML dinamice.

3. Funcționalități

Aplicația include următoarele funcționalități:

Introducerea numelui unui oraș prin intermediul unui formular.
Trimiterea numelui orașului către ruta /submit, utilizând metoda HTTP POST.
Afișarea numelui orașului selectat.
Afișarea temperaturii și a descrierii condițiilor meteorologice.
Prezentarea vitezei vântului, exprimată în kilometri pe oră.
Afișarea unor elemente vizuale sugestive pentru vreme, precum simbolul meteorologic și pictograma vântului.
Introducerea și transmiterea unei valori suplimentare prin formularul asociat rutei /ceva.
Utilizarea unor variabile dinamice pentru afișarea datelor primite de la server.
4. Tehnologii

Proiectul utilizează următoarele tehnologii:

Python – limbaj de programare utilizat pentru implementarea logicii aplicației, procesarea cererilor HTTP și integrarea cu servicii externe de furnizare a datelor meteorologice.

FastAPI – framework web modern pentru Python, utilizat pentru dezvoltarea backend-ului și gestionarea endpoint-urilor aplicației, oferind performanță ridicată și suport pentru validarea datelor și documentarea automată a API-urilor.

HTML5 – pentru structurarea paginii web, definirea formularelor și organizarea elementelor de conținut.

CSS3 – pentru stilizarea interfeței, culori, spațiere, colțuri rotunjite, umbre și alinierea elementelor.

Template-uri HTML (Jinja2) – variabilele precum {{oras}}, {{temperatura}}, {{vreme}} și {{viteza_vant}} permit introducerea dinamică a datelor furnizate de server în interfața utilizator.

HTTP/HTTPS – protocol utilizat pentru transmiterea datelor între client și server.

5. Arhitectură

Aplicația este implementată conform unei arhitecturi client-server bazate pe tehnologii web moderne. Componenta frontend realizează interacțiunea cu utilizatorul, iar backend-ul dezvoltat în Python FastAPI procesează cererile și furnizează datele necesare afișării informațiilor meteorologice.

Componente principale
Frontend (HTML/CSS) – interfața utilizatorului și formularele de introducere a datelor.
Backend FastAPI – gestionează rutele aplicației (/submit, /ceva), procesează cererile utilizatorului și pregătește datele pentru afișare.
Motor de șabloane Jinja2 – generează dinamic paginile HTML pe baza datelor furnizate de backend.
Serviciu extern de date meteorologice (API meteo) – furnizează informațiile meteorologice utilizate de aplicație.
Browser client – afișează rezultatele și permite interacțiunea cu sistemul.
Schema arhitecturală
Plain Text
┌─────────────────────┐
│ Browser Client │
│ Utilizator │
└──────────┬──────────┘
│ HTTP Request
▼
┌─────────────────────┐
│ Frontend HTML/CSS │
│ Formulare │
└──────────┬──────────┘
│
▼
┌─────────────────────┐
│ Python FastAPI │
│ Backend │
└───────┬───────┬─────┘
│ │
│ ▼
│ ┌─────────────┐
│ │ Jinja2 │
│ │ Templates │
│ └──────┬──────┘
│ │
▼ │
┌─────────────────────┐
│ API Meteo Extern │
└─────────────────────┘
│
▼
Date procesate și
afișate utilizatorului
Flux operațional
Utilizatorul introduce numele unui oraș în interfața web.
Formularul transmite cererea către endpoint-ul FastAPI prin metoda HTTP POST.
Backend-ul procesează cererea și interoghează serviciul meteorologic extern.
Datele obținute sunt transmise către șablonul Jinja2.
Pagina HTML este generată dinamic și returnată browserului.
Utilizatorul vizualizează informațiile meteorologice actualizate.

Această arhitectură asigură o separare clară între stratul de prezentare, logica aplicației și sursa de date, facilitând mentenanța, scalabilitatea și extinderea ulterioară a sistemului.

6. Instalare

Pentru vizualizarea și rularea aplicației sunt necesare un editor de cod, precum Visual Studio Code, și un browser web modern.

Pașii de instalare și pornire sunt:

Se salvează fișierele proiectului într-un director local.
Se deschide proiectul într-un editor de cod pentru verificare și modificare.
Se instalează dependențele necesare aplicației Python:
Shell
pip install fastapi uvicorn jinja2
Se pornește serverul FastAPI utilizând comanda:
Shell
uvicorn main:app --reload
Aplicația poate fi accesată prin browser la adresa configurată de serverul FastAPI.

Deschiderea directă a fișierului HTML nu este suficientă pentru funcționarea completă a formularelor și a afișării datelor dinamice, deoarece acestea depind de procesarea realizată de backend.

7. Utilizare

Utilizarea aplicației presupune următorii pași:

Utilizatorul accesează pagina aplicației prin intermediul browserului.
În primul formular, introduce numele orașului pentru care dorește să consulte informațiile meteorologice.
Apasă butonul „Afișează starea vremii”.
Cererea este trimisă către server prin ruta /submit.
După procesarea cererii, interfața afișează numele orașului, temperatura, condițiile meteorologice și viteza vântului.
Formularul suplimentar permite introducerea unei valori și transmiterea acesteia către ruta /ceva.
8. Testare

Testarea aplicației poate fi realizată prin verificarea aspectului vizual, a formularelor și a comunicării cu serverul.

Testele recomandate sunt:

Testarea interfeței: verificarea afișării corecte a cardului meteorologic, a titlurilor, a temperaturii și a vitezei vântului.

Testarea formularului pentru oraș: introducerea unui nume de oraș și verificarea transmiterii cererii către /submit.

Testarea formularului suplimentar: introducerea unei valori și verificarea transmiterii acesteia către /ceva.

Testarea câmpului obligatoriu: verificarea comportamentului formularului suplimentar atunci când câmpul este gol.

Testarea afișării dinamice: verificarea înlocuirii variabilelor de șablon cu valorile furnizate de server.

Testarea aspectului adaptiv: verificarea afișării paginii pe ecrane cu dimensiuni diferite.

Testarea endpoint-urilor FastAPI: verificarea funcționării rutelor /submit și /ceva, precum și a răspunsurilor generate de server pentru diferite valori de intrare.

Testarea integrării cu API-ul meteo: verificarea obținerii și afișării corecte a datelor meteorologice.

9. Limitări

Versiunea prezentată are următoarele limitări:

Documentația descrie arhitectura generală a aplicației, însă detaliile complete privind implementarea backend-ului și integrarea cu serviciul meteorologic nu sunt prezentate.

Nu sunt specificate mecanismele de autentificare sau protecție împotriva accesului neautorizat.

Variabilele dinamice depind de motorul de șabloane și de valorile furnizate de server.

Nu este inclusă validarea completă a numelui orașului sau tratarea tuturor erorilor de conectare.

Formularul suplimentar transmite o valoare către ruta /ceva, însă scopul și rezultatul acestei operații nu sunt detaliate.

Interfața utilizează stiluri CSS care pot necesita reorganizare pentru proiecte de dimensiuni mai mari.

Nu sunt implementate funcționalități precum prognoza pe mai multe zile, salvarea orașelor favorite sau actualizarea automată a datelor.

10. Dezvoltări viitoare

Proiectul poate fi extins prin implementarea următoarelor funcționalități:

Integrarea unui API meteorologic avansat pentru obținerea datelor actualizate și a prognozelor detaliate.

Adăugarea prognozei meteo pentru următoarele zile.

Afișarea unor informații suplimentare, precum umiditatea, presiunea atmosferică și temperatura resimțită.

Implementarea validării avansate a datelor introduse și a mesajelor de eroare pentru orașe inexistente sau indisponibilitatea serviciului.

Îmbunătățirea designului adaptiv pentru telefoane, tablete și calculatoare.

Separarea completă a componentelor frontend și backend pentru o arhitectură mai modulară.

Adăugarea unor teste automate pentru interfață și pentru endpoint-urile FastAPI.

Implementarea unui mecanism de memorare a orașelor căutate frecvent.

11. Autori

Autor: Ipati Veronica

12. Licență

Aplicația a fost dezvoltată în scop educațional, utilizând atât componente proprii, cât și servicii software furnizate de terți. Funcționalitatea sistemului se bazează pe integrarea tehnologiilor Python, FastAPI, Uvicorn, HTTPX și OpenWeatherMap.

Responsabilitatea pentru conținutul codului sursă și al documentației revine autorului proiectului. În cazul utilizării unor resurse externe, acestea trebuie menționate corespunzător și utilizate în conformitate cu termenii de utilizare impuși de furnizorii acestora.

Prezenta documentație reflectă versiunea actuală a aplicației și trebuie revizuită ori de câte ori sunt implementate modificări semnificative la nivelul funcționalităților sau arhitecturii sistemului.