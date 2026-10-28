import os
from pickletools import read_uint1

import requests
import re
import smtplib #pip3 install smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
import datetime
import sqlite3 #pip3 isntall sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
url = "https://www.emag.ro/memorie-ram-g-skill-96gb-ddr5-5600mhz-f5-5600j4040d48gx2-rs5k/pd/DGNTTTYBM/"
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "nume_produs": verifica_informatiile(url)[1],
            "pret_actual": verifica_informatiile(url)[0],
            "timestamp": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
            "url_produs": url,
            "pret_minim": calculeaza_minim_maxim_numar()[0],
            "pret_maxim": calculeaza_minim_maxim_numar()[1],
            "numar_verificari":calculeaza_minim_maxim_numar()[2],
            "continut_db": afiseaza_continut_db()
        }
    )
load_dotenv()
email_expeditor = os.getenv("EMAIL_EXPEDITOR")
app_password = os.getenv("APP_PASSWORD")

def trimite_email(destinatar,subiect,continut):
    mesaj= MIMEText(continut,"plain","utf-8")
    mesaj["Subject"] = subiect
    mesaj["From"] = email_expeditor
    mesaj["To"] = destinatar
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as email:
        email.login(email_expeditor,app_password)
        email.sendmail(email_expeditor,destinatar,mesaj.as_string())
    return True


def verifica_informatiile (url):
    antet_cerere = {"User-Agent":"Mozilla/5.0"}
    raspuns_server= requests.get(url,headers=antet_cerere,timeout=15)
    raspuns_server.raise_for_status()
    pagina_html = BeautifulSoup(raspuns_server.text, "html.parser")
    pret = pagina_html.find("p",class_="product-new-price")
    nume_produs = (pagina_html.find("h1",class_="page-title")).get_text(strip=True)
    if pret is None:
        print("PRETUL NU A FOST GASIT")
        return  None
    text_pret = pret.find(string=True,recursive=False).strip()
    # nume_produs = nume_produs(string=True,recursive=False)
    if text_pret is None:
        return None
    text_pret = int(re.sub(r"\D","",text_pret))
    return text_pret,nume_produs

def salvare_pret(pret):
    conexiune = sqlite3.connect("/Users/spikecsi/Desktop/BS4/pret.db")
    cursor = conexiune.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pret (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pret INTEGER NOT NULL,
    data_verificare TEXT NOT NULL
    )
    """)
    cursor.execute("""
    INSERT INTO pret (pret,data_verificare)
        VALUES (?,?)
    """,(pret,datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    conexiune.commit()
    cursor.close()
    print("Informatiile au fost salvate")

def afiseaza_continut_db():
    conexiune = sqlite3.connect("/Users/spikecsi/Desktop/BS4/pret.db")
    conexiune.row_factory = sqlite3.Row
    cursor = conexiune.cursor()
    cursor.execute("""
    SELECT * FROM pret
    """)
    rezultat = cursor.fetchall()
    lista = [dict(i) for i in rezultat]
    conexiune.close()
    return lista

def calculeaza_minim_maxim_numar():
    conexiune = sqlite3.connect("/Users/spikecsi/Desktop/BS4/pret.db")
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT MIN(pret), MAX(pret),COUNT(pret) FROM pret
    """)

    rezultat = cursor.fetchone()

    conexiune.close()

    return rezultat[0], rezultat[1], rezultat[2]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
