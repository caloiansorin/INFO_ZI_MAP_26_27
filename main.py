from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import requests
from starlette.responses import RedirectResponse
from urllib.parse import quote


load_dotenv()
cheie_api_openweather = os.getenv("API_KEY")
from fastapi import FastAPI, Request, Form,Query
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="items")

@app.post("/submit")
async def submit(oras: str = Form("Iasi")):
    oras = oras.strip()

    return RedirectResponse(
        url=f"/?oras={quote(oras, safe='')}",
        status_code=303
    )
# @app.post("/ceva")
# async def submit(request: Request, ceva: str = Form(...)):
#     return RedirectResponse(
#         url=f"?ceva={ceva}",
#         status_code=303
#     )

@app.get("/")
def home(request: Request,oras: str = Query("Iasi"), ceva: str = ""):
    oras = oras.strip()
    vremea, temperatura, viteza_vant = afisare_vreme(oras)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
        "vreme":vremea,
        "temperatura":temperatura,
        "viteza_vant":viteza_vant,
        "oras":oras,
        "mesaj":ceva
                 }
    )

def raspuns_geocoding(oras=""):
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


