
import re
import sqlite3
import datetime
from pathlib import Path
from urllib.parse import urlsplit

import requests
from bs4 import BeautifulSoup

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

import uvicorn


# CONFIGURARE
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "pret.db"

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# INITIALIZARE BAZA DE DATE
def initializare_db():

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pret (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pret REAL NOT NULL,
            data_verificare TEXT NOT NULL,
            nume_produs TEXT,
            url_produs TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(pret)")
    coloane = [col[1] for col in cursor.fetchall()]

    if "nume_produs" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN nume_produs TEXT"
        )

    if "url_produs" not in coloane:
        cursor.execute(
            "ALTER TABLE pret ADD COLUMN url_produs TEXT"
        )

    conexiune.commit()
    conexiune.close()


initializare_db()


# SEPARARE URL-URI
def separa_urluri(text):

    urluri = re.split(r"[\s,;|]+", text.strip())

    rezultat = []
    vazute = set()

    for url in urluri:

        url = url.strip()

        if url and url not in vazute:
            rezultat.append(url)
            vazute.add(url)

    return rezultat


# EXTRAGERE PRET
def extrage_pret(text):

    if not text:
        return None

    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()

    match = re.search(
        r"(\d[\d.]*)\s*,\s*(\d{1,2})",
        text
    )

    if match:

        partea_intreaga = match.group(1).replace(".", "")

        return float(
            f"{partea_intreaga}.{match.group(2)}"
        )

    match = re.search(r"\d[\d.]*", text)

    if match:
        return float(match.group().replace(".", ""))

    return None


# VERIFICARE LINK
def verifica_informatiile(url):

    if len(url) > 2048:
        raise ValueError("Linkul este prea lung.")

    parsed_url = urlsplit(url)

    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname not in (
            "emag.ro",
            "www.emag.ro"
        )
    ):
        raise ValueError(
            "Introdu un link valid de pe emag.ro."
        )

    antet_cerere = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
    }

    raspuns = requests.get(
        url,
        headers=antet_cerere,
        timeout=20,
        allow_redirects=False
    )

    raspuns.raise_for_status()

    pagina = BeautifulSoup(
        raspuns.text,
        "html.parser"
    )

    # NUME PRODUS
    element_nume = pagina.find(
        "h1",
        class_="page-title"
    )

    if element_nume is None:
        raise ValueError(
            "Numele produsului nu a fost gasit."
        )

    nume_produs = element_nume.get_text(strip=True)

    # PRET PRODUS
    element_pret = pagina.find(
        "p",
        class_="product-new-price"
    )

    pret = None

    if element_pret:

        pret = extrage_pret(
            element_pret.get_text(" ", strip=True)
        )

    if pret is None:

        meta_pret = pagina.find(
            "meta",
            attrs={"itemprop": "price"}
        )

        if meta_pret:

            pret = extrage_pret(
                meta_pret.get("content", "")
            )

    if pret is None:
        raise ValueError(
            "Pretul produsului nu a fost gasit."
        )

    return pret, nume_produs


# SALVARE PRET
def salvare_pret(pret, nume_produs, url_produs):

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        INSERT INTO pret
        (pret, data_verificare, nume_produs, url_produs)
        VALUES (?, ?, ?, ?)
    """, (
        pret,
        datetime.datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        ),
        nume_produs,
        url_produs
    ))

    conexiune.commit()
    conexiune.close()


# VERIFICARE UN SINGUR PRODUS
def verifica_un_produs(url):

    rezultat = {
        "url": url,
        "nume_produs": "-",
        "pret": None,
        "status": "Eroare",
        "mesaj": ""
    }

    try:

        pret, nume_produs = verifica_informatiile(url)

        salvare_pret(
            pret,
            nume_produs,
            url
        )

        rezultat["nume_produs"] = nume_produs
        rezultat["pret"] = pret
        rezultat["status"] = "Succes"
        rezultat["mesaj"] = "Produs verificat cu succes."

    except requests.RequestException as e:

        print(f"Eroare la accesarea {url}: {e}")

        rezultat["mesaj"] = (
            "Nu am putut accesa pagina eMAG."
        )

    except ValueError as e:

        rezultat["mesaj"] = str(e)

    except Exception as e:

        print(f"Eroare: {e}")

        rezultat["mesaj"] = (
            "A aparut o eroare neasteptata."
        )

    return rezultat


# ISTORIC
def afiseaza_continut_db():

    conexiune = sqlite3.connect(DB_PATH)
    conexiune.row_factory = sqlite3.Row

    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT *
        FROM pret
        ORDER BY id DESC
        LIMIT 50
    """)

    rezultat = cursor.fetchall()

    conexiune.close()

    return [dict(i) for i in rezultat]


# STATISTICI
def calculeaza_minim_maxim_numar():

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT MIN(pret), MAX(pret), COUNT(pret)
        FROM pret
    """)

    rezultat = cursor.fetchone()

    conexiune.close()

    return rezultat[0], rezultat[1], rezultat[2]


# CONTEXT HTML
def obtine_context(
    rezultate=None,
    eroare=None,
    succes=None,
    url_introdus="",
    urluri_multiple=""
):

    istoric = afiseaza_continut_db()

    ultimul_produs = istoric[0] if istoric else None

    minim, maxim, numar = calculeaza_minim_maxim_numar()

    return {
        "ultimul_produs": ultimul_produs,
        "pret_minim": minim,
        "pret_maxim": maxim,
        "numar_verificari": numar,
        "continut_db": istoric,
        "rezultate": rezultate or [],
        "eroare": eroare,
        "succes": succes,
        "url_introdus": url_introdus,
        "urluri_multiple": urluri_multiple
    }


# PAGINA PRINCIPALA
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=obtine_context()
    )


# RUTA VERIFICARE INDIVIDUALA
@app.post("/verifica-unul", response_class=HTMLResponse)
async def verifica_unul(request: Request):

    form = await request.form()

    url = str(
        form.get("url_produs", "")
    ).strip()

    if not url:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=obtine_context(
                eroare="Introdu un link de produs.",
                url_introdus=url
            )
        )

    rezultat = verifica_un_produs(url)

    eroare = None
    succes = None

    if rezultat["status"] == "Succes":
        succes = rezultat["mesaj"]
    else:
        eroare = rezultat["mesaj"]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=obtine_context(
            rezultate=[rezultat],
            eroare=eroare,
            succes=succes,
            url_introdus=url
        )
    )


# RUTA VERIFICARE MULTIPLA
@app.post("/verifica", response_class=HTMLResponse)
async def verifica_multiple(request: Request):

    form = await request.form()

    text_urluri = str(
        form.get("urluri", "")
    ).strip()

    urluri = separa_urluri(text_urluri)

    if not urluri:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=obtine_context(
                eroare="Introdu cel putin un link.",
                urluri_multiple=text_urluri
            )
        )

    if len(urluri) > 50:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=obtine_context(
                eroare="Poti verifica maximum 50 de linkuri odata.",
                urluri_multiple=text_urluri
            )
        )

    rezultate = []

    for url in urluri:

        rezultat = verifica_un_produs(url)

        rezultate.append(rezultat)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=obtine_context(
            rezultate=rezultate,
            urluri_multiple=text_urluri
        )
    )


# STERGERE ISTORIC
@app.post("/sterge/{produs_id}")
def sterge_produs(produs_id: int):

    conexiune = sqlite3.connect(DB_PATH)
    cursor = conexiune.cursor()

    cursor.execute(
        "DELETE FROM pret WHERE id = ?",
        (produs_id,)
    )

    conexiune.commit()
    conexiune.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
