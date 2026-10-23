from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import unicodedata

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# Cache pentru lista de localități.
_lista_orase = None


def normalizeaza(text):
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        caracter for caracter in text
        if unicodedata.category(caracter) != "Mn"
    )
    return text.casefold().strip()


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "items" / "home.html")


def cauta_coordonate(oras):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    raspuns = requests.get(
        url,
        params={
            "q": oras,
            "limit": 10,
            "appid": API_KEY
        },
        timeout=10
    )

    raspuns.raise_for_status()
    return raspuns.json()


def incarca_orase():
    global _lista_orase

    if _lista_orase is not None:
        return _lista_orase

    url = (
        "https://raw.githubusercontent.com/"
        "mariuspopescu/romanian-cities/master/cities.json"
    )

    try:
        raspuns = requests.get(url, timeout=15)
        raspuns.raise_for_status()
        date = raspuns.json()

        orase = []

        for item in date:
            if isinstance(item, dict):
                nume = (
                    item.get("name")
                    or item.get("city")
                    or item.get("nume")
                )

                if nume:
                    orase.append({
                        "nume": nume,
                        "tara": "România",
                        "state": item.get("county", "")
                    })

        if not orase:
            raise ValueError("Lista de orașe este goală.")

        # Eliminăm duplicatele.
        unice = {}
        for oras in orase:
            cheie = normalizeaza(oras["nume"])
            unice.setdefault(cheie, oras)

        _lista_orase = sorted(
            unice.values(),
            key=lambda oras: normalizeaza(oras["nume"])
        )

        return _lista_orase

    except (requests.RequestException, ValueError, TypeError):
        _lista_orase = [
            {"nume": nume, "tara": "România", "state": ""}
            for nume in [
                "Bacău", "Baia Mare", "Bistrița", "Botoșani",
                "Brăila", "Brașov", "București", "Buzău",
                "Cluj-Napoca", "Constanța", "Craiova", "Iași",
                "Oradea", "Piatra Neamț", "Pitești", "Ploiești",
                "Sibiu", "Suceava", "Timișoara"
            ]
        ]

        return _lista_orase


@app.get("/sugestii")
def sugestii(oras: str = ""):
    text = oras.strip()

    if not text:
        return []

    localitati = incarca_orase()
    prefix = normalizeaza(text)

    rezultate = [
        locatie for locatie in localitati
        if normalizeaza(locatie["nume"]).startswith(prefix)
    ]

    return rezultate[:50]


@app.get("/mesaj")
def mesaj(oras: str = "Bacau"):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Cheia API_KEY lipsește din fișierul .env."
        )

    try:
        rezultate = cauta_coordonate(oras)

        rezultate_romania = [
            locatie for locatie in rezultate
            if locatie.get("country") == "RO"
        ]

        if not rezultate_romania:
            raise HTTPException(
                status_code=404,
                detail="Nu am găsit acest oraș în România."
            )

        locatie = rezultate_romania[0]

        lat = locatie["lat"]
        lon = locatie["lon"]

        raspuns = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "ro"
            },
            timeout=10
        )

        raspuns.raise_for_status()
        date = raspuns.json()

    except HTTPException:
        raise

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Nu am putut prelua datele meteo."
        )

    return {
        "oras": locatie["name"],
        "tara": "România",
        "lat": lat,
        "long": lon,
        "temperatura": round(date["main"]["temp"]),
        "descriere": date["weather"][0]["description"],
        "conditie": date["weather"][0]["main"]
    }