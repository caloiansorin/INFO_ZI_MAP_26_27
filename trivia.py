# eu sunt cartoful smecher
from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import requests
load_dotenv()
cheie_api_openweather = os.getenv("API_KEY")
app = FastAPI()
@app.get("/")
def home():
    return FileResponse("items/home.html")

def raspuns_geocoding(oras):
    url_geocoding = "http://api.openweathermap.org/geo/1.0/direct?"
    raspuns = requests.get(url_geocoding, params={
        'q': oras,
        'appid': cheie_api_openweather
    }).json()
    return raspuns


def afisare_vreme(oras):
    url = "https://api.openweathermap.org/data/2.5/weather?"
    lat = raspuns_geocoding(oras)[0]['lat']
    lon = raspuns_geocoding(oras)[0]['lon']
    raspuns = requests.get(url,params={
        'lat':lat,
        'lon':lon,
        'appid':cheie_api_openweather,
        'units':'metric',
        'lang':'ro'
    }).json()
    starea_vremii = raspuns['weather'][0]['description']
    temperatura = raspuns['main']['temp']
    viteza_vant = raspuns['wind']['speed']
    return starea_vremii,temperatura,viteza_vant


@app.get("/mesaj")
def mesaj():
    return {"starea_vremii":afisare_vreme("Bacau"),
            "temperatura":afisare_vreme("Bacau"),
             "viteza_vant":afisare_vreme("Bacau")}


