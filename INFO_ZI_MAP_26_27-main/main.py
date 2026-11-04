import os
import re
import sqlite3
import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pret.db"

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)



def initializare_db():
    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pret (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nume_produs TEXT,
            link TEXT,
            pret INTEGER,
            data_verificare TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(pret)")
    coloane = {rand[1] for rand in cursor.fetchall()}

    if "nume_produs" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN nume_produs TEXT"
        )

    if "link" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN link TEXT"
        )

    if "pret" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN pret INTEGER"
        )

    if "data_verificare" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN data_verificare TEXT"
        )

    conexiune.commit()
    conexiune.close()



initializare_db()


def verifica_informatiile(link):

    domeniu = urlparse(link).hostname

    if not domeniu or not (
        domeniu == "emag.ro"
        or domeniu.endswith(".emag.ro")
    ):
        raise ValueError("Introdu un link valid de pe eMAG.")

    antet_cerere = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ro-RO,ro;q=0.9"
    }

    raspuns_server = requests.get(
        link,
        headers=antet_cerere,
        timeout=20
    )

    raspuns_server.raise_for_status()

    pagina_html = BeautifulSoup(
        raspuns_server.text,
        "html.parser"
    )

    nume_produs = None

    meta_titlu = pagina_html.find(
        "meta",
        property="og:title"
    )

    if meta_titlu:
        nume_produs = meta_titlu.get("content")

    if not nume_produs:
        titlu = pagina_html.find(
            "h1",
            class_="page-title"
        )

        if titlu:
            nume_produs = titlu.get_text(
                strip=True
            )

    if not nume_produs and pagina_html.title:
        nume_produs = pagina_html.title.get_text(
            strip=True
        )

    if not nume_produs:
        nume_produs = "Produs eMAG"

    pret_text = None

    meta_pret = pagina_html.find(
        "meta",
        property="product:price:amount"
    )

    if meta_pret:
        pret_text = meta_pret.get("content")

    if not pret_text:
        pret_element = pagina_html.find(
            "p",
            class_="product-new-price"
        )

        if pret_element:
            pret_text = pret_element.get_text(
                strip=True
            )

    if not pret_text:
        pret_element = pagina_html.find(
            "meta",
            itemprop="price"
        )

        if pret_element:
            pret_text = pret_element.get("content")

    pret_numeric = None

    if pret_text:
        cifre = re.sub(r"[^\d]", "", pret_text)

        if cifre:
            pret_numeric = int(cifre)

    return {
        "nume": nume_produs,
        "pret": pret_numeric,
        "link": link
    }


def salvare_pret(nume_produs, link, pret):

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        INSERT INTO pret (
            nume_produs,
            link,
            pret,
            data_verificare
        )
        VALUES (?, ?, ?, ?)
    """, (
        nume_produs,
        link,
        pret,
        datetime.datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    ))

    conexiune.commit()
    conexiune.close()


def afiseaza_continut_db():

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT * FROM pret
        ORDER BY id DESC
    """)

    rezultat = cursor.fetchall()

    conexiune.close()

    return rezultat


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    istoric = afiseaza_continut_db()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "nume_produs": "Niciun produs selectat",
            "pret_actual": "-",
            "timestamp": "-",
            "numar_verificari": len(istoric),
            "istoric": istoric,
            "produs_cautat": None,
            "eroare": None
        }
    )

@app.post("/cauta-produs", response_class=HTMLResponse)
def cauta_produs(
    request: Request,
    link_produs: str = Form(...)
):

    linkuri = [
        link.strip()
        for link in link_produs.split(";")
        if link.strip()
    ]

    produse = []
    erori = []

    for link in linkuri:

        try:

            produs = verifica_informatiile(link)

            if produs["pret"] is not None:

                salvare_pret(
                    produs["nume"],
                    produs["link"],
                    produs["pret"]
                )

                produs["pret_afisat"] = (
                    str(produs["pret"]) + " lei"
                )

            else:
                produs["pret_afisat"] = "Pret indisponibil"

            produse.append(produs)

        except requests.RequestException:
            erori.append(
                f"Nu am putut accesa produsul: {link}"
            )

        except ValueError as e:
            erori.append(str(e))

        except Exception as e:
            erori.append(
                f"Eroare pentru {link}: {str(e)}"
            )

    istoric = afiseaza_continut_db()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "produse": produse,
            "istoric": istoric,
            "numar_verificari": len(istoric),
            "eroare": " | ".join(erori) if erori else None,
            "nume_produs": "",
            "pret_actual": "",
            "timestamp": datetime.datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            "produs_cautat": None
        }
    )


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )