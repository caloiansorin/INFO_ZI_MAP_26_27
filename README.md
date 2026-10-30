# SimpleWeatherApp

Aplicație web simplă pentru afișarea vremii curente într-un oraș ales de utilizator.

## 1. Titlul proiectului

**SimpleWeatherApp — aplicație web pentru consultarea vremii curente**

## 2. Descriere

SimpleWeatherApp permite utilizatorului să caute un oraș și să consulte câteva informații despre vremea curentă: temperatura în grade Celsius, descrierea condițiilor meteo și viteza vântului. Dacă nu este introdus un oraș, aplicația afișează implicit vremea din Iași.

Aplicația folosește serviciul OpenWeatherMap pentru a identifica orașul și a prelua datele meteo. Informațiile sunt afișate într-o pagină web cu o interfață compactă. Proiectul se concentrează pe vremea curentă; nu oferă prognoze pentru zilele următoare.

## 3. Funcționalități

- Căutarea vremii după numele orașului.
- Afișarea orașului căutat, a temperaturii, a descrierii vremii și a vitezei vântului.
- Afișarea implicită a vremii pentru Iași la accesarea paginii fără un oraș specificat.
- Prezentarea descrierilor meteo în limba română.

## 4. Tehnologii

- **Python** — limbajul folosit pentru logica aplicației.
- **FastAPI** — gestionează rutele web și formularul de căutare. Este potrivit pentru un proiect mic, oferă o structură clară pentru endpoint-uri și se integrează cu validarea datelor din formulare.
- **Jinja2** — generează pagina HTML folosind un șablon și valorile meteo obținute de server. Astfel, datele pot fi afișate direct în pagina returnată de aplicație.
- **OpenWeatherMap API** — furnizează coordonatele orașului și datele despre vremea curentă.
- **Requests** — trimite cereri HTTP către API.
- **python-dotenv** — încarcă cheia API din fișierul local `.env`, în loc să fie scrisă în cod.
- **Uvicorn** — pornește serverul ASGI folosit pentru rularea aplicației.

## 5. Arhitectură

Proiectul are o structură restrânsă:

```text
.
├── main.py          # aplicația FastAPI și cererile către OpenWeatherMap
├── items/
│   └── index.html   # șablonul Jinja2 și interfața web
├── .env             # cheia API locală; nu se publică
└── README.md        # documentația proiectului
```

La căutare, formularul trimite numele orașului către server. Aplicația cere coordonatele orașului de la serviciul de geocodare OpenWeatherMap, apoi folosește coordonatele pentru a obține vremea curentă. Valorile primite sunt transmise șablonului Jinja2 pentru afișare.

## 6. Ghid de instalare

### Cerințe

- Python instalat.
- O cheie API OpenWeatherMap.
- Conexiune la internet.

### Pași de instalare în Windows PowerShell

Clonează repository-ul și intră în directorul proiectului:

```powershell
git clone https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git
cd INFO_ZI_MAP_26_27
```

Creează și activează un mediu virtual, apoi instalează dependențele:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn requests python-dotenv jinja2 python-multipart
```

Creează un fișier `.env` în directorul principal și adaugă cheia API:

```env
API_KEY=cheia_ta_openweathermap
```

Nu publica fișierul `.env` și nu trimite cheia API în repository. Pornește serverul:

```powershell
python -m uvicorn main:app --reload
```

Deschide [http://127.0.0.1:8000](http://127.0.0.1:8000) în browser. Oprirea serverului se face cu `Ctrl+C` în terminal.

## 7. Ghid de utilizare

La deschiderea aplicației este afișată vremea pentru Iași. Pentru a căuta alt oraș, introdu numele acestuia în câmpul de căutare și apasă **„Afișează starea vremii”**. Pagina se reîncarcă și prezintă datele returnate de API pentru orașul căutat.

Capturi de ecran realizate în timpul testării:

**Pagina inițială — vremea pentru Iași**

![Pagina inițială a aplicației, cu vremea pentru Iași](screenshots/weather-default.png)

**Rezultatul căutării pentru București**

![Rezultatul căutării vremii pentru București](screenshots/weather-bucharest.png)

Valorile meteo din capturi sunt exemple din momentul testării și se pot schimba.

## 8. Testare

Aplicația a fost pornită local și verificată manual prin browser și cereri HTTP:

| Verificare | Rezultat |
|---|---|
| Deschiderea paginii fără oraș (`GET /`) | Reușită — pagina afișează date pentru Iași |
| Căutarea unui oraș (`GET /?oras=Bucharest`) | Reușită — pagina afișează datele returnate pentru București |
| Trimiterea formularului de oraș (`POST /submit`) | Reușită — serverul răspunde cu `303` și redirecționează la rezultatul căutării |
| Trimiterea celui de-al doilea formular (`POST /ceva`) | Eșuată — serverul răspunde cu `404`, deoarece ruta nu este implementată |

Testele care folosesc API-ul necesită o cheie OpenWeatherMap validă și acces la internet. Răspunsurile meteo sunt date live, deci valorile exacte nu sunt constante.

## 9. Limitări

- Al doilea formular din pagină nu funcționează: trimite date către ruta `/ceva`, care nu există în aplicație.
- Viteza vântului este returnată de OpenWeatherMap în metri pe secundă pentru unitățile metrice, dar interfața o etichetează `km/h`; conversia unității nu este implementată.
- Aplicația nu afișează prognoze, umiditate sau temperatura resimțită.
- Este necesară conexiunea la OpenWeatherMap și o cheie API validă.
- Tratarea orașelor inexistente și a erorilor API nu este implementată complet; în astfel de cazuri, cererea poate eșua.

## 10. Dezvoltări viitoare

Posibile îmbunătățiri pentru versiuni viitoare:

- Eliminarea celui de-al doilea formular sau implementarea rutei corespunzătoare.
- Corectarea afișării vitezei vântului prin conversie în `km/h` sau schimbarea etichetei în `m/s`.
- Adăugarea unor mesaje clare pentru orașe negăsite, chei API invalide și indisponibilitatea serviciului meteo.
- Adăugarea prognozei pentru zilele următoare și a altor indicatori meteo.
- Mutarea dependențelor într-un fișier `requirements.txt` pentru instalare mai ușoară.

## 11. Autori

- **Cimbriciuc-Nichita**

## 12. Licență

Proiectul este distribuit sub licența **MIT**, care permite folosirea, modificarea și redistribuirea codului, cu păstrarea notificării de copyright și a textului licenței. Consultă fișierul [LICENSE](LICENSE) pentru termenii compleți.
