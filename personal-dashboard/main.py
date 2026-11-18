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


@app.get("/")
def radacina():
    """Ruta / ne trimite direct la /home."""
    return RedirectResponse("/home")


@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")
