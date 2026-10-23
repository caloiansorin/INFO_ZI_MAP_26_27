# INFO_ZI_MAP_26_27

## 1. Titlul proiectului

INFO_ZI_MAP_26_27 – Aplicație web pentru monitorizarea condițiilor meteorologice

## 2. Descriere

Acest proiect are ca scop dezvoltarea unei aplicații web care permite utilizatorului să introducă un oraș și să primească informații despre starea vremii în timp real. Aplicația utilizează date dintr-o sursă externă de meteorologie și le afișează într-un mod simplu, clar și ușor de utilizat.

Proiectul a fost realizat în contextul lucrării de laborator / proiectului de studiu, având rolul de a demonstra integrarea dintre frontend, backend și API extern.

## 3. Funcționalități

- introducerea numelui unui oraș;
- obținerea coordonatelor geografice ale orașului;
- preluarea datelor meteorologice din OpenWeatherMap;
- afișarea temperaturii, vitezei vântului și descrierii stării vremii;
- gestionarea erorilor pentru orașuri nevalide sau lipsa cheii API;
- interfață web simplă, inspirată de un formular de căutare și rezultatul afișat pentru utilizator.

## 4. Tehnologii

- Python
- FastAPI
- Jinja2
- Requests
- Dotenv
- HTML / CSS / template rendering
- OpenWeatherMap API

## 5. Arhitectură

Proiectul este structurat pe două niveluri principale:

- Backend: aplicația FastAPI gestionează rutele, primește datele de la utilizator și face cereri către API-ul extern.
- Frontend: template-ul HTML este renderizat prin Jinja2 și afișează rezultatele în browser.

Fluxul principal:

1. utilizatorul introduce un oraș;
2. serverul validează inputul;
3. aplicația caută coordonatele orașului prin geocoding;
4. se face o cerere către OpenWeatherMap pentru date meteo;
5. rezultatul este transmis către template-ul HTML și afișat utilizatorului.

## 6. Instalare

1. Clonează proiectul:

   bash
   git clone https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git
   cd INFO_ZI_MAP_26_27

2. Creează un mediu virtual:

   bash
   python -m venv .venv
   source .venv/bin/activate

3. Instalează dependențele:

   bash
   pip install -r requirements.txt

4. Creează fișierul `.env` și adaugă cheia API:

   env
   API_KEY=cheia_ta_de_la_openweather

5. Rulează aplicația:

   bash
   uvicorn trivia:app --reload

## 7. Utilizare

După pornirea aplicației, deschide browserul și accesează:

http://127.0.0.1:8000/

Introdu un oraș în câmpul disponibil și apasă pentru a obține datele meteo. Exemple de orașe: București, Cluj-Napoca, Iași, Timișoara.

## 8. Testare

Pentru validarea funcționalității, se recomandă:

- verificarea apelurilor către API;
- testarea cazurilor cu oraș valid și oraș invalid;
- verificarea comportamentului când cheia API lipsește;
- teste manuale prin accesarea aplicației în browser.

Într-un proiect extins, se poate adăuga un set de teste automate cu pytest.

## 9. Limitări

- depinde de disponibilitatea serviciului OpenWeatherMap;
- necesită o cheie API validă;
- datele sunt limitate la informațiile oferite de API-ul extern;
- aplicația este simplă și nu include funcții avansate precum istoricul meteo, grafice sau notificări.

## 10. Dezvoltări viitoare

- adăugarea unui istoric al căutărilor;
- afișarea prognozei pe 5 zile;
- suport pentru mai multe limbi;
- introducerea unei interfete mai moderne și responsive;
- salvarea preferințelor utilizatorului;
- integrarea cu alte surse de date meteorologice.

## 11. Autori

- Sabau Daniel - Student la ,, Universitatea Vasile Alecsandri din Bacau "
- Proiect realizat în scop educațional / de studiu

## 12. Licență

Acest proiect este distribuit sub o licență deschisa.
