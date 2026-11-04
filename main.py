import requests
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
from email.mime.text import MIMEText
import smtplib
import sqlite3
import os
import datetime
import time
from urllib.parse import urlparse
from jinja2 import Environment, FileSystemLoader
load_dotenv()  # Load environment variables from .env file
email_expeditor = os.getenv("EMAIL_EXPEDITOR")
app_password = os.getenv("APP_PASSWORD")
#<p class="product-new-price"

def trimite_email(destinatar,subiect,continut):
    mesaj = MIMEText(continut, "plain", "utf-8")
    mesaj["Subject"] = subiect
    mesaj["From"] = email_expeditor
    mesaj["To"] = destinatar
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, timeout=15) as email:
        email.login(email_expeditor, app_password)
        email.send_message(mesaj)
        return True

# Pune aici produsele verificate cand rulezi direct main.py (cate un link pe rand)
URLURI = [
    "https://www.emag.ro/memorie-ram-g-skill-96gb-ddr5-5600mhz-f5-5600j4040d48gx2-rs5k/pd/DGNTTTYBM/",
]
MAX_LINKURI = 10  # cate linkuri accepta formularul odata
PAUZA_INTRE_CERERI = 3  # secunde; eMAG da captcha daca primeste cereri prea repede
nume_produs = None
def verifica_informatiile(url):
    global nume_produs
    antet_cere = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    raspuns_server = requests.get(url, headers=antet_cere,timeout= 15)
    # eMAG raspunde cu 511 + pagina captcha cand detecteaza prea multe cereri
    if raspuns_server.status_code == 511 or "eMAG Captcha" in raspuns_server.text[:500]:
        return "Blocat de eMAG (captcha). Mai incearca peste cateva ore."
    raspuns_server.raise_for_status()
    pagina_html = BeautifulSoup(raspuns_server.text, features="html.parser")
    nume_produs = pagina_html.find("h1", class_="page-title").get_text(strip=True)
    print(nume_produs)
    pret = pagina_html.find("p", class_="product-new-price")
    if pret is None:
        return "Nu s-a putut găsi prețul produsului."
    text_pret = pret.find(string=True, recursive=False)
    if text_pret is None:
        return None
    text_pret = int(re.sub(r"[^\d]", "", text_pret))
    # clasa gtm_... se schimba de la produs la produs, asa ca cautam doar dupa "rating-text"
    rating = None
    nr_recenzii = 0
    element_rating = pagina_html.find("a", class_="rating-text")
    if element_rating is not None:
        text_rating = element_rating.find(string=True, recursive=False)
        if text_rating and text_rating.strip():
            rating = float(text_rating.strip())
        span_recenzii = element_rating.find("span")
        if span_recenzii is not None:
            cifre = re.sub(r"[^\d]", "", span_recenzii.get_text())
            nr_recenzii = int(cifre) if cifre else 0
    return text_pret, rating, nr_recenzii

# <h1 class="page-title" data-test="page-title">
# #<a href="#reviews-section" class="rating-text gtm_rp101318">
#  5.00
#   <span>(1 review)</span>
#</a>
# Memorie RAM, G.SKILL, 96GB, DDR5, 5600MHz
#       </h1>



def salvare_pret(nume, pret, data_ora):
    conexiune = sqlite3.connect("pret.db")
    cursor = conexiune.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pret (id INTEGER PRIMARY KEY AUTOINCREMENT, nume_produs TEXT, pret INTEGER NOT NULL, data_verificare TEXT NOT NULL);")
    # daca tabelul exista deja din versiunea veche (fara nume), adaugam coloana
    coloane = [rand[1] for rand in cursor.execute("PRAGMA table_info(pret)")]
    if "nume_produs" not in coloane:
        cursor.execute("ALTER TABLE pret ADD COLUMN nume_produs TEXT")
    cursor.execute("INSERT INTO pret (nume_produs, pret, data_verificare) VALUES (?, ?, ?)", (nume, pret, data_ora))
    conexiune.commit()  # fara commit nu se salveaza nimic in baza de date
    conexiune.close()


def citeste_istoric():
    conexiune = sqlite3.connect("pret.db")
    conexiune.row_factory = sqlite3.Row  # ca sa putem scrie rand.pret in template
    cursor = conexiune.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pret (id INTEGER PRIMARY KEY AUTOINCREMENT, nume_produs TEXT, pret INTEGER NOT NULL, data_verificare TEXT NOT NULL);")
    istoric = cursor.execute("SELECT id, nume_produs, pret, data_verificare FROM pret ORDER BY id DESC").fetchall()
    conexiune.close()
    return istoric


def este_link_emag(link):
    adresa = urlparse(link)
    gazda = adresa.hostname or ""
    return adresa.scheme in ("http", "https") and (gazda == "emag.ro" or gazda.endswith(".emag.ro"))


def curata_linkuri(valori):
    # un camp poate contine mai multe linkuri lipite; scoatem si dublurile, pastrand ordinea
    linkuri = []
    for valoare in valori:
        for link in valoare.split():
            if link not in linkuri:
                linkuri.append(link)
    return linkuri


def verifica_produs(link):
    global nume_produs
    nume_produs = None  # verifica_informatiile scrie numele aici
    produs = {"url": link, "nume": None, "pret": None, "rating": None, "nr_recenzii": 0,
              "data_ora": None, "eroare": None, "blocat": False}
    try:
        rezultat = verifica_informatiile(link)
    except Exception as e:
        produs["eroare"] = f"Nu am putut citi pagina: {e}"
        return produs
    produs["nume"] = nume_produs
    if not isinstance(rezultat, tuple):
        produs["eroare"] = rezultat or "Nu s-a putut citi prețul produsului."
        produs["blocat"] = bool(rezultat) and rezultat.startswith("Blocat")
        return produs
    produs["pret"], produs["rating"], produs["nr_recenzii"] = rezultat
    produs["data_ora"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ora locala (Romania)
    salvare_pret(produs["nume"], produs["pret"], produs["data_ora"])
    return produs


def verifica_lista(linkuri):
    # verificam pe rand, cu pauza; daca eMAG ne blocheaza, nu mai trimitem alte cereri
    produse = []
    blocat = False
    cerere_facuta = False
    for link in linkuri:
        if not este_link_emag(link):
            produse.append({"url": link, "eroare": "Nu este un link de pe emag.ro."})
        elif blocat:
            produse.append({"url": link, "eroare": "Neverificat: eMAG a blocat cererile anterioare."})
        else:
            if cerere_facuta:
                time.sleep(PAUZA_INTRE_CERERI)
            produs = verifica_produs(link)
            cerere_facuta = True
            blocat = produs["blocat"]
            produse.append(produs)
    return produse


def puncte_grafic(randuri, latime=320, inaltime=64, margine=8):
    # transforma ultimele 30 de preturi in coordonate pentru graficul SVG
    randuri = randuri[-30:]
    preturi = [rand["pret"] for rand in randuri]
    minim, maxim = min(preturi), max(preturi)
    puncte = []
    for i, rand in enumerate(randuri):
        x = latime - margine if len(randuri) == 1 else margine + i * (latime - 2 * margine) / (len(randuri) - 1)
        y = inaltime / 2 if minim == maxim else inaltime - margine - (rand["pret"] - minim) * (inaltime - 2 * margine) / (maxim - minim)
        puncte.append({"x": round(x, 1), "y": round(y, 1), "pret": rand["pret"], "data": rand["data_verificare"]})
    return puncte


def analizeaza_randuri(randuri):
    # randuri = verificarile unui produs, de la cea mai veche la cea mai noua
    preturi = [rand["pret"] for rand in randuri]
    curent = preturi[-1]
    minim, maxim = min(preturi), max(preturi)
    medie = sum(preturi) / len(preturi)
    anterior = preturi[-2] if len(preturi) > 1 else None
    diferenta = curent - anterior if anterior is not None else None
    procent = diferenta / anterior * 100 if anterior else None

    if len(preturi) == 1:
        verdict, ton = "Prima verificare", "neutru"
    elif minim == maxim:
        verdict, ton = "Preț stabil", "neutru"
    elif curent == minim:
        verdict, ton = "Cel mai mic preț", "bun"
    elif curent == maxim:
        verdict, ton = "Cel mai mare preț", "rau"
    elif curent < medie:
        verdict, ton = "Sub medie", "bun"
    else:
        verdict, ton = "Peste medie", "rau"

    return {"curent": curent, "minim": minim, "maxim": maxim, "medie": round(medie),
            "diferenta": diferenta, "procent": procent, "nr_verificari": len(preturi),
            "verdict": verdict, "ton": ton, "puncte": puncte_grafic(randuri)}


def grupeaza_istoric(istoric):
    # istoric vine cu cele mai noi randuri primele, deci produsul verificat recent apare primul
    grupuri = {}
    for rand in istoric:
        grupuri.setdefault(rand["nume_produs"] or "Produs fără nume", []).append(rand)
    return [{"nume": nume, "randuri": randuri, "analiza": analizeaza_randuri(randuri[::-1])}
            for nume, randuri in grupuri.items()]


def construieste_date_pagina(produse=(), linkuri=(), aviz=None):
    grupuri = grupeaza_istoric(citeste_istoric())
    analize = {grup["nume"]: grup["analiza"] for grup in grupuri}
    for produs in produse:
        if produs["eroare"] is None:
            produs["analiza"] = analize.get(produs["nume"] or "Produs fără nume")

    reusite = [produs for produs in produse if produs["eroare"] is None]
    cu_rating = [produs for produs in reusite if produs["rating"] is not None]
    rezumat = None
    if produse:
        comparatie = len(reusite) > 1  # "cel mai ieftin" are sens doar intre cel putin doua produse
        rezumat = {
            "total": len(produse),
            "reusite": len(reusite),
            "ieftin": min(reusite, key=lambda p: p["pret"]) if comparatie else None,
            "cotat": max(cu_rating, key=lambda p: (p["rating"], p["nr_recenzii"])) if comparatie and cu_rating else None,
        }
    return {"produse": produse, "rezumat": rezumat, "grupuri": grupuri, "linkuri": list(linkuri),
            "aviz": aviz, "max_linkuri": MAX_LINKURI}


def genereaza_pagina(date_pagina):
    # index.html ramane sablonul, rezultatul se scrie in pagina.html
    mediu = Environment(loader=FileSystemLoader("."), autoescape=True)
    pagina = mediu.get_template("index.html").render(**date_pagina)
    with open("pagina.html", "w", encoding="utf-8") as fisier:
        fisier.write(pagina)


def text_email(produse):
    linii = []
    for produs in produse:
        if produs["eroare"] is None:
            rating = f"{produs['rating']:.2f} ({produs['nr_recenzii']} recenzii)" if produs["rating"] is not None else "fara rating"
            linii.append(f"{produs['nume']}\npretul este: {produs['pret']} LEI\nrating: {rating}\ndata: {produs['data_ora']}\n")
        else:
            linii.append(f"{produs['url']}\neroare: {produs['eroare']}\n")
    return "\n".join(linii)


#  • ort 587: TLS / STARTTLS (Recommended for most apps and clients)
#• Port 465: SSL / Implicit TLS (Supported as an alternative or for legacy
if __name__ == "__main__":
    produse = verifica_lista(URLURI)
    genereaza_pagina(construieste_date_pagina(produse, URLURI))
    reusite = sum(1 for produs in produse if produs["eroare"] is None)
    if reusite:
        trimite_email(email_expeditor, f"Preturi eMAG: {reusite} din {len(produse)} produse verificate", text_email(produse))

# Mai multe URL-uri si sa afiseze informatiile pentru url uri
