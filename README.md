# Caiet de sarcini: „Personal Dashboard”

**Tehnologii:** Python, FastAPI, Jinja2, requests

**Ce primiți:** folderul `personal-dashboard`, care conține un `main.py` gol și frontend-ul gata făcut (`templates/index.html` și `templates/style.css`). Toate datele din pagină sunt scrise direct în HTML.

**Ce aveți de făcut:** pas cu pas, fiecare element din dashboard trebuie să ajungă să afișeze date reale, venite din backend și din API-uri publice. Nu modificați designul; lucrați doar pe structura HTML, șabloanele Jinja2 și backend.

**Regulă:** totul se face în Python. Nu se folosește JavaScript.

**API-uri de folosit (Puteți folosi oricare alt API înlocuitor.):**

- Open-Meteo, vreme și căutare oraș: https://open-meteo.com/en/docs
- Frankfurter, curs valutar: https://frankfurter.dev
- ZenQuotes, citatul zilei: https://zenquotes.io
- Nager.Date, sărbători legale: https://date.nager.at

---

## Etapa 0: Pregătire

- [ ] Creează un mediu virtual Python și instalează `fastapi`, `jinja2` și `requests`.
- [ ] Configurează `.env` și `.gitignore`

## Etapa 1: Rutele de bază

- [ ] Creează ruta `/home`.
- [ ] Creează ruta `/`, care redirecționează către `/home`.

## Etapa 2: Dashboard-ul servit de FastAPI

- [ ] Afișează `index.html` pe `/home`, randat cu Jinja2.
- [ ] Fă `style.css` să se încarce prin FastAPI.
- [ ] Împarte `index.html` într-un șablon de bază și câte un șablon separat pentru fiecare card. (Jinja2!!!)

## Etapa 3: Antetul

- [ ] Afișează data de azi, în română, generată în backend.
- [ ] Afișează salutul potrivit orei („Bună dimineața”, „Bună ziua”, „Bună seara”).
- [ ] Fă ceasul să arate ora la care s-a încărcat pagina.
- [ ] Fă logo-ul și linkul „Acasă” să ducă la dashboard.

## Etapa 4: Cardul „Sarcinile zilei”

- [ ] Înlocuiește cele 5 sarcini scrise în HTML cu o listă trimisă din backend. (Lista simplă, fără DB)
- [ ] Fă formularul de adăugare să funcționeze (titlu și prioritate).
- [ ] Fă butonul de bifare să funcționeze: o sarcină bifată apare tăiată, iar la al doilea click se debifează.
- [ ] Fă butonul de ștergere să funcționeze.
- [ ] Fă eticheta de prioritate să aibă culoarea corespunzătoare.
- [ ] Calculează textul „X din Y finalizate” și lățimea barei de progres.
- [ ] Afișează un mesaj când nu există nicio sarcină.
- [ ] Ordonează sarcinile: întâi cele nefinalizate, apoi după prioritate.
- [ ] Salvează sarcinile într-o bază de date SQLite, ca să nu se piardă la repornirea serverului.

## Etapa 5: Cardul „Vremea”

- [ ] Afișează vremea curentă pentru București, cu date de la Open-Meteo.
- [ ] Afișează pictograma și descrierea în română, potrivite codului de vreme primit.
- [ ] Completează vântul, umiditatea și temperaturile minimă și maximă.
- [ ] Fă formularul de căutare să funcționeze pentru orice oraș; după căutare, câmpul păstrează orașul căutat.
- [ ] Afișează numele orașului găsit și țara.
- [ ] Afișează prognoza pe următoarele 5 zile, cu numele zilelor în română.
- [ ] Afișează un mesaj în card când orașul nu există.
- [ ] Afișează ora reală a ultimei actualizări.

## Etapa 6: Cardul „Curs valutar”

- [ ] Afișează cursurile reale EUR, USD și GBP față de RON, cu date de la Frankfurter.
- [ ] Afișează data cursului.
- [ ] Fă convertorul să funcționeze pentru orice combinație de monede.
- [ ] După conversie, păstrează în formular suma și monedele alese.
- [ ] Afișează sumele în format românesc (virgulă zecimală, două zecimale).
- [ ] Tratează sumele invalide (negative, goale).

## Etapa 7: Cardul „Citatul zilei”

- [ ] Afișează citatul zilei și autorul, cu date de la ZenQuotes.
- [ ] Cere citatul de la API cel mult o dată pe zi; în rest, refolosește-l.

## Etapa 8: Cardul „Următoarea sărbătoare”

- [ ] Afișează următoarea sărbătoare legală din România, cu date de la Nager.Date.
- [ ] Calculează câte zile mai sunt; scrie corect „azi”, „mâine”, „1 zi” și „X zile”.
- [ ] Afișează data sărbătorii în română (de exemplu „Luni, 30 noiembrie 2026”).
- [ ] Afișează în listă următoarele două sărbători, fără să afișezi de două ori aceeași sărbătoare.

## Etapa 9: Organizarea codului și robustețe

- [ ] Separă codul pe module: rute, apeluri către API-uri, baza de date.
- [ ] Mută setările (orașul implicit, monedele, timeout-ul) într-un fișier de configurare.
- [ ] Când un API e căzut sau lent, doar cardul lui afișează un mesaj; restul dashboard-ului funcționează.
- [ ] Păstrează în cache răspunsul fiecărui API un timp rezonabil, ca să nu faci request-uri la fiecare reîncărcare.

## Etapa 10: Predare

- [ ] Scrie un `README.md`: descriere, capturi de ecran, pașii de instalare și rulare.
