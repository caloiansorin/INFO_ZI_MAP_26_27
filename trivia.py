
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()
jinja_env = Environment(loader=FileSystemLoader("items"))


def get_api_key():
    return os.getenv("API_KEY")


def raspuns_geocoding(oras: str):
    cheie_api_openweather = get_api_key()
    if not cheie_api_openweather:
        raise ValueError("API_KEY nu este setat. Adaugă cheia în fișierul .env.")

    url_geocoding = "http://api.openweathermap.org/geo/1.0/direct"
    raspuns = requests.get(
        url_geocoding,
        params={"q": oras, "appid": cheie_api_openweather},
        timeout=10,
    )
    raspuns.raise_for_status()
    date = raspuns.json()

    if not date:
        raise ValueError(f"Nu am găsit orașul {oras}.")

    return date[0]


def afisare_vreme(oras: str):
    cheie_api_openweather = get_api_key()
    locatie = raspuns_geocoding(oras)
    url = "https://api.openweathermap.org/data/2.5/weather"
    raspuns = requests.get(
        url,
        params={
            "lat": locatie["lat"],
            "lon": locatie["lon"],
            "appid": cheie_api_openweather,
            "units": "metric",
            "lang": "ro",
        },
        timeout=10,
    )
    raspuns.raise_for_status()
    vreme = raspuns.json()

    return {
        "starea_vremii": vreme["weather"][0]["description"],
        "temperatura": vreme["main"]["temp"],
        "viteza_vant": vreme["wind"]["speed"],
    }


@app.get("/")
def home(request: Request, oras: str | None = None):
    date = None
    eroare = None

    if oras:
        try:
            date = afisare_vreme(oras)
        except ValueError as exc:
            eroare = str(exc)
        except Exception:
            eroare = "Eroare la preluarea datelor meteo. Verifică numele orașului sau cheia API."

    html = jinja_env.get_template("home.html").render(
        request=request,
        oras=oras,
        date=date,
        eroare=eroare,
    )
    return HTMLResponse(content=html)


@app.get("/mesaj")
def mesaj(oras: str = "Bacau"):
    return afisare_vreme(oras)


