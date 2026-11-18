# uvicorn main:app --reload
# pip3 install --upgrade uvicorn websockets
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
numele_tau = os.getenv("NUME", "prietene")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def salut():
    acum = datetime.now()
    ora = acum.hour
    if ora < 12:
        mesaj = "Bună dimineața"
    elif ora < 18:
        mesaj = "Bună ziua"
    else:
        mesaj = "Bună seara"
    return f"{mesaj}, {numele_tau}! Ora curentă este: {acum.strftime('%Y-%m-%d %H:%M')}"

def belwo_bunaziua():
    ZILE = ["Luni", "Marți", "Miercuri", "Joi", "Vineri", "Sâmbătă", "Duminică"]
    LUNI = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", 
        "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]
    acum = datetime.now()
    zi = ZILE[acum.weekday()]    
    luna = LUNI[acum.month - 1]   
    return f"{zi}, {acum.day} {luna} {acum.year}"

@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    text_salut = salut()
    print(text_salut)
    return templates.TemplateResponse(request, "index.html", {"salut": text_salut})