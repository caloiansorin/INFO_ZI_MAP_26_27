import os
import logging

import requests
import re
import smtplib #pip3 install smtplib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.mime.text import MIMEText
import datetime
import sqlite3 #pip3 isntall sqlite3
from urllib.parse import urlparse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pret.db")
logger = logging.getLogger(__name__)
app = FastAPI()
templates = Jinja2Templates(directory="templates")
@app.get("/")
def home(request: Request, product_urls: str = ""):
    results = []
    cleaned_text = product_urls.strip()
    parts = re.split(r"[;\s]+", cleaned_text)
    urls = []
    for item in parts:
        if item:
            urls.append(item)
    for product_url in urls:
        result = {"url": product_url}
        try:
            parsed_url = urlparse(product_url)
            hostname = parsed_url.hostname or ""
            if parsed_url.scheme not in ("http", "https") or not (
                hostname == "emag.ro" or hostname.endswith(".emag.ro")
            ):
                result["error"] = "Introdu un link valid de pe emag.ro."
            else:
                pret_actual, nume_produs = verifica_informatiile(product_url)
                result.update({
                    "pret": pret_actual,
                    "nume": nume_produs,
                    "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                })
        except (requests.RequestException, ValueError) as exc:
            logger.warning("Could not read the eMAG product at %s: %s", product_url, exc)
            result["error"] = "Nu am putut citi produsul. Verifica linkul sau incearca din nou."

        results.append(result)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results,
            "product_urls": product_urls,
        }
    )
load_dotenv()
email_expeditor = os.getenv("EMAIL_EXPEDITOR")
app_password = os.getenv("APP_PASSWORD")

def trimite_email(destinatar,subiect,continut):
    if not email_expeditor or not app_password:
        raise RuntimeError("EMAIL_EXPEDITOR and APP_PASSWORD must be set to send email.")

    mesaj= MIMEText(continut,"plain","utf-8")
    mesaj["Subject"] = subiect
    mesaj["From"] = email_expeditor
    mesaj["To"] = destinatar
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as email:
        email.login(email_expeditor,app_password)
        email.sendmail(email_expeditor,destinatar,mesaj.as_string())
    return True


def verifica_informatiile (url: str) -> tuple[int, str]:
    antet_cerere = {"User-Agent":"Mozilla/5.0"}
    raspuns_server= requests.get(url,headers=antet_cerere,timeout=15)
    raspuns_server.raise_for_status()
    pagina_html = BeautifulSoup(raspuns_server.text, "html.parser")
    pret = pagina_html.find("p",class_="product-new-price")
    titlu_produs = pagina_html.find("h1",class_="page-title")
    if titlu_produs is None:
        raise ValueError("Product title was not found on the page.")
    if pret is None:
        raise ValueError("Product price was not found on the page.")
    nume_produs = titlu_produs.get_text(strip=True)
    text_pret = pret.find(string=True,recursive=False)
    if text_pret is None:
        raise ValueError("Product price text was not found on the page.")
    text_pret = text_pret.strip()
    text_pret = int(re.sub(r"\D","",text_pret))
    return text_pret,nume_produs

def salvare_pret(pret):
    conexiune = sqlite3.connect(database_path)
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
    conexiune = sqlite3.connect(database_path)
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
    conexiune = sqlite3.connect(database_path)
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT MIN(pret), MAX(pret),COUNT(pret) FROM pret
    """)

    rezultat = cursor.fetchone()

    conexiune.close()

    return rezultat[0], rezultat[1], rezultat[2]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
