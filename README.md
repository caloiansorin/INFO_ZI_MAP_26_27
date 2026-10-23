# Documentație tehnică

## 1. Titlul proiectului

**Vremea Acum** – aplicație web pentru afișarea vremii.

## 2. Descriere

Aplicația afișează vremea curentă pentru un oraș introdus de utilizator. Datele meteo sunt preluate de la serviciul OpenWeatherMap.

## 3. Funcționalități

- căutarea vremii după numele orașului;
- afișarea temperaturii, a stării vremii și a vitezei vântului;
- afișarea vremii pentru orașul Iași la deschiderea paginii.

## 4. Tehnologii

| Tehnologie | În locul | Motivul alegerii |
|---|---|---|
| Python | PHP, JavaScript | Are o sintaxă simplă și este studiat la școală. |
| FastAPI | Flask, Django | Necesită mai puțin cod; Django este prea complex pentru o aplicație mică. |
| Uvicorn | Gunicorn | Este serverul recomandat pentru FastAPI. |
| Jinja2 | React | Afișează datele în pagină fără a folosi JavaScript. |
| requests | urllib | Este mai ușor de utilizat. |
| python-dotenv | cheia scrisă în cod | Cheia API nu este publicată pe GitHub. |
| OpenWeatherMap | Open-Meteo | Este gratuit și oferă descrierea vremii în limba română. |
| HTML și CSS | React, Bootstrap | Sunt suficiente pentru o singură pagină. |

## 5. Arhitectură

Utilizatorul introduce orașul în pagină. Serverul FastAPI află coordonatele orașului, solicită vremea de la OpenWeatherMap și afișează rezultatul în pagina HTML.

```
INFO_ZI_MAP_26_27/
├── main.py
├── items/
│   └── index.html
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## 6. Instalare

```bash
git clone https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git
cd INFO_ZI_MAP_26_27
pip install -r requirements.txt
```

În folderul proiectului se creează fișierul `.env`, care conține cheia API de la OpenWeatherMap:

```
API_KEY=cheia_api
```

## 7. Utilizare

```bash
uvicorn main:app --reload
```

Se deschide în browser adresa http://127.0.0.1:8000, se introduce numele orașului și se apasă butonul **Afișează starea vremii**.

## 8. Testare

Aplicația a fost testată manual, în browser:

| Test | Rezultat |
|---|---|
| Deschiderea paginii | Se afișează vremea pentru Iași. |
| Introducerea unui oraș existent | Se afișează vremea pentru orașul introdus. |
| Introducerea unui oraș cu diacritice | Se afișează vremea corect. |
| Introducerea unui oraș inexistent | Apare o eroare. |

## 9. Limitări

- pentru un oraș inexistent apare o eroare, fără un mesaj explicativ;
- viteza vântului este afișată în km/h, deși valoarea primită este în m/s;
- pictograma vremii nu se modifică.

## 10. Dezvoltări viitoare

- afișarea unui mesaj atunci când orașul nu este găsit;
- prognoza pentru următoarele zile;
- pictograme diferite în funcție de vreme.

## 11. Autori

Sandu Yanis

## 12. Licență

Proiectul este distribuit sub licența GNU GPL v3.0.
