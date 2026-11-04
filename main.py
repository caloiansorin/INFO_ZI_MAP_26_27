import datetime
import os
import re
import smtplib
import sqlite3
from email.mime.text import MIMEText

import requests
import uvicorn
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

import produs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pret.db")
URL = "https://www.emag.ro/memorie-ram-g-skill-96gb-ddr5-5600mhz-f5-5600j4040d48gx2-rs5k/pd/DGNTTTYBM/"
FORMAT_DATA = "%d/%m/%Y %H:%M:%S"

load_dotenv()
email_expeditor = os.getenv("EMAIL_EXPEDITOR")
app_password = os.getenv("APP_PASSWORD")

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


def trimite_email(destinatar, subiect, continut):
    mesaj = MIMEText(continut, "plain", "utf-8")
    mesaj["Subject"] = subiect
    mesaj["From"] = email_expeditor
    mesaj["To"] = destinatar
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(email_expeditor, app_password)
        email.sendmail(email_expeditor, destinatar, mesaj.as_string())
    return True


def parseaza_pret(element):
    """Din <p class="product-new-price">1.899<sup>99</sup> <span>Lei</span></p>
    intoarce 1899.99 (float). Intoarce None daca nu se poate citi."""
    lei_text = element.find(string=True, recursive=False)
    if lei_text is None:
        return None
    lei = re.sub(r"\D", "", lei_text)
    if not lei:
        return None
    bani_tag = element.find("sup")
    bani = re.sub(r"\D", "", bani_tag.get_text()) if bani_tag else ""
    return float(f"{lei}.{bani[:2].ljust(2, '0')}") if bani else float(lei)


def verifica_informatiile(url):
    """Intoarce (pret, nume_produs) sau (None, None) daca pagina nu are datele."""
    antet_cerere = {"User-Agent": "Mozilla/5.0"}
    raspuns = requests.get(url, headers=antet_cerere, timeout=15)
    raspuns.raise_for_status()
    pagina = BeautifulSoup(raspuns.text, "html.parser")

    element_pret = pagina.find("p", class_="product-new-price")
    element_nume = pagina.find("h1", class_="page-title")
    if element_pret is None or element_nume is None:
        print("PRETUL SAU NUMELE NU AU FOST GASITE")
        return None, None

    return parseaza_pret(element_pret), element_nume.get_text(strip=True)


def conectare_db():
    conexiune = sqlite3.connect(DB_PATH)
    conexiune.execute("""
        CREATE TABLE IF NOT EXISTS pret (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pret REAL NOT NULL,
            data_verificare TEXT NOT NULL
        )
    """)
    return conexiune


def salvare_pret(pret):
    conexiune = conectare_db()
    with conexiune:
        conexiune.execute(
            "INSERT INTO pret (pret, data_verificare) VALUES (?, ?)",
            (pret, datetime.datetime.now().strftime(FORMAT_DATA)),
        )
    conexiune.close()


def citeste_istoric(limita=50):
    conexiune = conectare_db()
    randuri = conexiune.execute(
        "SELECT id, pret, data_verificare FROM pret ORDER BY id DESC LIMIT ?", (limita,)
    ).fetchall()
    stats = conexiune.execute("SELECT MIN(pret), MAX(pret), COUNT(*) FROM pret").fetchone()
    conexiune.close()
    return randuri, stats


def formateaza_pret(valoare):
    if valoare is None:
        return "-"
    text = f"{valoare:,.2f}"
    # 1,899.99 -> 1.899,99
    text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    if text.endswith(",00"):
        text = text[:-3]
    return f"{text} lei"


templates.env.filters["pret"] = formateaza_pret


@app.get("/")
def home(request: Request):
    eroare = None
    nume_produs = "Produs necunoscut"
    pret_actual = None
    try:
        pret_actual, nume = verifica_informatiile(URL)
        if nume:
            nume_produs = nume
        if pret_actual is not None:
            salvare_pret(pret_actual)
        else:
            eroare = "Nu am gasit pretul pe pagina eMAG."
    except requests.RequestException as e:
        eroare = f"Eroare la accesarea eMAG: {e}"

    istoric, (pret_min, pret_max, nr_verificari) = citeste_istoric()
    if pret_actual is None and istoric:
        pret_actual = istoric[0][1]  # ultimul pret salvat

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "nume_produs": nume_produs,
            "pret_actual": pret_actual,
            "url": URL,
            "timestamp": datetime.datetime.now().strftime(FORMAT_DATA),
            "pret_min": pret_min,
            "pret_max": pret_max,
            "nr_verificari": nr_verificari,
            "istoric": istoric,
            "eroare": eroare,
        },
    )


@app.get("/adauga")
def adauga(request: Request, urls: str = ""):
    produse, mesaj = produs.descarca_multiple(urls)
    return templates.TemplateResponse(
        request=request,
        name="adauga.html",
        context={"urls": urls, "produse": produse, "mesaj": mesaj},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
