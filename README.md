# Documentație tehnică

## 1. Titlul proiectului

**Vremea Acum (WeatherApp)** – aplicație web meteo scrisă în Python cu FastAPI.

## 2. Descriere

Aplicația afișează vremea curentă pentru orașul introdus de utilizator: temperatura, starea vremii (în română) și viteza vântului. Serverul transformă numele orașului în coordonate și cere datele de la [OpenWeatherMap](https://openweathermap.org/).

## 3. Funcționalități

- Căutarea vremii după numele orașului, printr-un formular (`POST /submit`).
- Oraș implicit **Iasi**, la deschiderea paginii și când formularul este trimis gol.
- Afișarea temperaturii în grade Celsius, a stării vremii în română și a vitezei vântului.
- Link direct către rezultat: `/?oras=<nume>`.
- Suport pentru diacritice și spații în plus (`strip()` și `quote`).

## 4. Tehnologii

| Tehnologie | În loc de | De ce |
|---|---|---|
| Python | PHP, JavaScript | Este mai simplu și îl știu de la școală. |
| FastAPI | Flask, Django | Se scrie cu mai puțin cod. Django este prea mare pentru o aplicație mică. |
| Uvicorn | Gunicorn | Este serverul recomandat pentru FastAPI. |
| Jinja2 | React | Pune datele în pagină fără JavaScript. |
| requests | urllib | Este mai ușor de folosit. |
| python-dotenv | Cheia scrisă în cod | Cheia API nu ajunge pe GitHub. |
| OpenWeatherMap | Open-Meteo | Este gratuit și dă descrierea vremii în română. |
| HTML + CSS | React, Bootstrap | Pentru o singură pagină nu e nevoie de mai mult. |

## 5. Arhitectură

```
Browser  ──HTTP──▶  FastAPI (main.py)  ──requests──▶  OpenWeatherMap
   ▲                    │                              ├─ Geocoding API  (oraș → lat, lon)
   └──── HTML ◀── Jinja2 (items/index.html)            └─ Weather API    (lat, lon → vremea)
```

### Structura proiectului

```
INFO_ZI_MAP_26_27/
├── main.py
├── items/
│   └── index.html
├── requirements.txt
├── .env
├── .gitignore
├── LICENSE
└── README.md
```

### Fluxul unei cereri

1. Formularul trimite orașul la `POST /submit`.
2. Serverul răspunde cu redirect **303** către `/?oras=<oraș>`.
3. `home()` apelează `afisare_vreme(oras)`.
4. `raspuns_geocoding(oras)` află latitudinea și longitudinea.
5. Se cere vremea curentă pentru aceste coordonate.
6. Jinja2 completează `index.html` și pagina este trimisă browserului.

## 6. Instalare

**Cerințe:** Python 3.10+ și o cheie API gratuită de la [OpenWeatherMap](https://home.openweathermap.org/users/sign_up).

```bash
git clone https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git
cd INFO_ZI_MAP_26_27
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Creează fișierul `.env` în folderul proiectului:

```
API_KEY=cheia_ta_openweathermap
```

> O cheie nouă poate avea nevoie de câteva ore până devine activă.

## 7. Utilizare

```bash
uvicorn main:app --reload
```

Deschide **http://127.0.0.1:8000**, scrie un oraș și apasă **Afișează starea vremii**. Un oraș se poate cere și direct: `http://127.0.0.1:8000/?oras=Bucuresti`.

## 8. Testare

Aplicația a fost testată manual, în browser:

| # | Scenariu | Rezultat |
|---|---|---|
| T1 | Deschiderea paginii `/` | Vremea pentru Iasi |
| T2 | Oraș valid: `Cluj-Napoca` | Vremea pentru Cluj-Napoca |
| T3 | Oraș cu diacritice: `Bacău` | Vremea pentru Bacău |
| T4 | Spații în plus: `  Iasi  ` | Spațiile sunt eliminate |
| T5 | Câmp gol | Vremea pentru Iasi |
| T6 | Oraș inexistent: `Xyzabc` | Eroare 500 |
| T7 | Fără `.env` sau cheie greșită | Eroare 500 |

## 9. Limitări

- Un oraș inexistent sau o cheie API greșită dau eroare 500, fără mesaj pentru utilizator.
- Viteza vântului vine în m/s, dar pagina scrie km/h.
- Temperatura se afișează fără `°C`.
- Geocodingul este apelat de două ori pentru aceeași căutare.
- Pictograma ⛅ nu se schimbă după vreme.
- Formularul „Introdu ceva” trimite către `/ceva`, rută care nu există (404).

## 10. Dezvoltări viitoare

- Mesaj „Orașul nu a fost găsit” în loc de eroarea 500.
- Vânt în km/h și `°C` la temperatură.
- Un singur apel de geocoding.
- Pictogramă după starea vremii.
- Prognoza pe 5 zile, umiditate și presiune.
- Teste automate cu `pytest`.

## 11. Autori

**Sandu Yanis** – dezvoltare, documentație

## 12. Licență

Proiectul este distribuit sub licența **GNU GPL v3.0**. Textul complet se află în fișierul `LICENSE`.

© 2026 Sandu Yanis
