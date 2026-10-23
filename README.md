#Basic Weather

#Descriere
Aplicatie web pentru afisarea informatiilor meteo ale unui oras, precum temperatura, starea vremii si viteza vantului.

#Tehnologii
Python – logica aplicatiei.
FastAPI – gestionarea cererilor HTTP.
Jinja2 – generarea paginilor HTML.
Requests – comunicarea cu API-ul extern.
OpenWeather API – furnizarea datelor meteo.
HTML/CSS – interfata utilizatorului.

#Arhitectura
main.py – logica si rutele aplicatiei.
items/ – sabloane HTML.
.env – cheia API.

Flux: Utilizator → FastAPI → OpenWeather API → Afisarea datelor.

#Instalare
git clone https://github.com/caloiansorin/INFO_ZI_MAP_26_27.git
cd INFO_ZI_MAP_26_27
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn requests python-dotenv jinja2 python-multipart

#IMPORTANT!!
Creeaza fisierul .env si adauga cheia API:

API_KEY=cheia_ta_openweather

#Porneste aplicatia
uvicorn main:app --reload

Acceseaza http://127.0.0.1:8000.

#Utilizare
Foloseste http://127.0.0.1:8000 in browser
Introdu numele unui oras.
Consulta informatiile meteo afisate.

#POZE(todo)

#Limitari
Necesita internet si o cheie API valida.
Datele depind de serviciul OpenWeather.
Functionalitatile meteo sunt limitate.

#Autor
Caldararu Alessandro

Copyright
© 2026 – Basic Weather. Toate drepturile rezervate.
