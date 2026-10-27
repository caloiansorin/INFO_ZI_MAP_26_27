# Documentație tehnică

## 1. Titlul proiectului

Aplicație Meteo – Verificarea vremii într-un oraș

## 2. Descriere

Proiectul este o aplicație meteo realizată în Python, cu ajutorul căreia poți afla cum este vremea într-un anumit oraș.

Utilizatorul scrie numele orașului într-un formular, iar aplicația caută informațiile despre vreme și le afișează pe pagină. Informațiile sunt preluate de la OpenWeather API.

Aplicația afișează:
- Numele orașului;
- Temperatura în grade Celsius;
- Descrierea vremii;
- Viteza vântului.

Dacă utilizatorul nu alege un oraș, aplicația afișează vremea din Iași.

## 3. Funcționalități

Aplicația poate:
- Să primească numele unui oraș de la utilizator.
- Să găsească coordonatele orașului.
- Să preia informațiile despre vreme folosind OpenWeather API.
- Să afișeze temperatura, starea vremii și viteza vântului.
- Să actualizeze informațiile atunci când utilizatorul caută alt oraș.
- Să afișeze datele într-o pagină web simplă și ușor de folosit.

## 4. Tehnologii utilizate

Pentru realizarea proiectului am folosit:
- **Python** – pentru partea de programare.
- **FastAPI** – pentru crearea aplicației web.
- **HTML** – pentru elementele paginii.
- **CSS** – pentru aspectul paginii.
- **Jinja2** – pentru afișarea datelor din Python în pagina HTML.
- **Requests** – pentru trimiterea cererilor către API.
- **OpenWeather API** – pentru obținerea informațiilor despre vreme.
- **python-dotenv** – pentru citirea cheii API din fișierul `.env`.
- **Uvicorn** – pentru pornirea aplicației.

## 5. Arhitectura aplicației

Proiectul conține următoarele fișiere:

- `main.py` – aici se află codul Python, funcțiile și rutele aplicației.
- `items/index.html` – pagina în care utilizatorul introduce orașul și vede informațiile despre vreme.
- `.env` – fișierul în care se salvează cheia API.
- `README.md` – fișierul în care este explicat proiectul.

### Cum funcționează aplicația?

1. Utilizatorul deschide aplicația în browser.
2. Introduce numele unui oraș în formular.
3. Apasă butonul pentru afișarea vremii.
4. Aplicația caută coordonatele orașului.
5. Folosește coordonatele pentru a obține datele despre vreme.
6. Afișează rezultatele pe pagină.

## 6. Instalare

Pentru a porni aplicația, este nevoie de Python, de o conexiune la internet și de o cheie API de la OpenWeather.

### Pași pentru instalare

1. Se deschide folderul proiectului în terminal.

2. Se creează un mediu virtual cu comanda:

   ```bash
   python -m venv .venv
   ```

3. Se activează mediul virtual în Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Se instalează bibliotecile folosite:

   ```bash
   pip install fastapi uvicorn requests python-dotenv jinja2 python-multipart
   ```

5. Se creează fișierul `.env` în folderul principal și se adaugă cheia API:

   ```env
   API_KEY=cheia_ta_openweather
   ```

   În loc de `cheia_ta_openweather` se introduce cheia personală obținută de la OpenWeather.

6. Se pornește aplicația cu:

   ```bash
   uvicorn main:app --reload
   ```

7. Se deschide browserul și se accesează adresa:

   `http://127.0.0.1:8000`

## 7. Utilizare

Pentru a folosi aplicația, utilizatorul trebuie să intre pe pagina principală, să scrie numele orașului dorit și să apese butonul „Afișează starea vremii”.

După aceea, aplicația afișează temperatura, descrierea vremii și viteza vântului pentru orașul introdus.

Dacă nu este specificat un oraș, se folosește implicit Iași.

## 8. Testare

Aplicația poate fi verificată prin câteva exemple:
- Se deschide pagina principală și se verifică dacă apare vremea pentru Iași.
- Se introduce un oraș valid și se verifică rezultatele.
- Se caută un alt oraș și se verifică dacă informațiile se schimbă.
- Se verifică dacă formularul funcționează corect.
- Se poate verifica ce se întâmplă dacă orașul nu există sau cheia API nu este validă.

Aceste verificări pot fi făcute manual, folosind aplicația în browser.

## 9. Limitări

Aplicația are câteva limitări:
- Este nevoie de internet pentru a obține datele despre vreme.
- Este nevoie de o cheie API validă.
- Dacă utilizatorul introduce un oraș care nu poate fi găsit, aplicația poate genera o eroare.
- Pictograma meteo este aceeași indiferent de vremea de afară.
- Nu sunt tratate toate erorile care pot apărea la conectarea cu API-ul.

## 10. Dezvoltări viitoare

Pe viitor, aplicația poate fi îmbunătățită prin:
- Adăugarea unor mesaje pentru orașele care nu sunt găsite.
- Schimbarea pictogramei în funcție de vreme.
- Afișarea prognozei pentru următoarele zile.
- Adăugarea unor informații precum umiditatea și presiunea atmosferică.
- Îmbunătățirea aspectului pe telefon.
- Salvarea orașelor căutate recent.

## 11. Autori

Amalia Bondrila Mihaela

## 12. Licență

Licența proiectului nu este stabilită momentan.