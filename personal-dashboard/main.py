# uvicorn main:app --reload
# pip3 install -- upgrade uvicorn websockets
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from dotenv import load_dotenv
import os
import time
from datetime import datetime
import requests

load_dotenv()
CHEIE_OPEN_WEATHER = os.getenv("OPEN_WEATHER_API_KEY")
numele_tau = os.getenv("NUME")
app = FastAPI()
templates = Jinja2Templates(directory="templates")


def salut(ora_curenta):
    ora_curenta = ora_curenta.strftime("%H")
    ora_curenta = int(ora_curenta)
    if ora_curenta < 12:
        return "Buna dimineata"
    else:
        if ora_curenta < 18:
            return "Buna ziua"
    return "Buna seara"


@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    acum = datetime.now()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"ora": acum.strftime("%H:%M"), "salut": salut(acum)},
    )
