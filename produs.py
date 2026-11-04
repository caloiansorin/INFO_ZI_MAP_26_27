"""Extrage datele unui produs de pe o pagina eMAG."""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ANTET = {"User-Agent": "Mozilla/5.0", "Accept-Language": "ro-RO,ro;q=0.9"}


class LinkInvalid(ValueError):
    pass


def valideaza_url(url):
    """Accepta doar linkuri https catre emag.ro (evita cereri catre alte site-uri)."""
    url = (url or "").strip()
    if url and "://" not in url:
        url = "https://" + url
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if p.scheme not in ("http", "https") or not (host == "emag.ro" or host.endswith(".emag.ro")):
        raise LinkInvalid("Introdu un link de produs de pe emag.ro")
    return url


def _pret_din_tag(tag):
    """<p>1.899<sup>99</sup> <span>Lei</span></p> -> 1899.99"""
    if tag is None:
        return None
    text = tag.find(string=True, recursive=False)
    lei = re.sub(r"\D", "", text or "")
    if not lei:
        return None
    sup = tag.find("sup")
    bani = re.sub(r"\D", "", sup.get_text()) if sup else ""
    return float(f"{lei}.{bani[:2].ljust(2, '0')}") if bani else float(lei)


def _json_ld_produs(pagina):
    """Intoarce dictionarul schema.org/Product din pagina, sau {}."""
    for script in pagina.find_all("script", type="application/ld+json"):
        try:
            date = json.loads(script.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        candidati = date if isinstance(date, list) else [date]
        for c in list(candidati):
            if isinstance(c, dict) and "@graph" in c:
                candidati.extend(c["@graph"])
        for c in candidati:
            if isinstance(c, dict) and c.get("@type") in ("Product", ["Product"]):
                return c
    return {}


def _numar(valoare):
    try:
        return float(str(valoare).replace(",", "."))
    except (TypeError, ValueError):
        return None


def parseaza_pagina(html):
    pagina = BeautifulSoup(html, "html.parser")
    ld = _json_ld_produs(pagina)
    oferta = ld.get("offers") or {}
    if isinstance(oferta, list):
        oferta = oferta[0] if oferta else {}

    # nume
    h1 = pagina.find("h1", class_="page-title")
    nume = h1.get_text(strip=True) if h1 else ld.get("name")

    # pret actual: intai din pagina, apoi din JSON-LD
    pret = _pret_din_tag(pagina.find("p", class_="product-new-price"))
    if pret is None:
        pret = _numar(oferta.get("price"))

    # pret vechi si reducere
    pret_vechi = _pret_din_tag(pagina.select_one("p.product-old-price s") or pagina.find("p", class_="product-old-price"))
    reducere = None
    if pret and pret_vechi and pret_vechi > pret:
        reducere = round((pret_vechi - pret) / pret_vechi * 100)
    else:
        pret_vechi = None

    # imagine
    imagine = ld.get("image")
    if isinstance(imagine, list):
        imagine = imagine[0] if imagine else None
    if not imagine:
        og = pagina.find("meta", property="og:image")
        imagine = og.get("content") if og else None

    # stoc
    stoc = None
    disp = str(oferta.get("availability", ""))
    if "InStock" in disp:
        stoc = "In stoc"
    elif "OutOfStock" in disp:
        stoc = "Stoc epuizat"
    else:
        eticheta = pagina.select_one("span[class*=label-in_stock], span[class*=label-out_of_stock], span[class*=label-limited_stock]")
        stoc = eticheta.get_text(strip=True) if eticheta else None

    # rating
    rating_ld = ld.get("aggregateRating") or {}
    rating = _numar(rating_ld.get("ratingValue"))
    nr_recenzii = rating_ld.get("reviewCount") or rating_ld.get("ratingCount")

    return {
        "nume": nume,
        "pret": pret,
        "pret_vechi": pret_vechi,
        "reducere": reducere,
        "imagine": imagine,
        "stoc": stoc,
        "rating": rating,
        "nr_recenzii": nr_recenzii,
    }


def descarca_produs(url):
    url = valideaza_url(url)
    raspuns = requests.get(url, headers=ANTET, timeout=15)
    raspuns.raise_for_status()
    date = parseaza_pagina(raspuns.text)
    if not date["nume"] and date["pret"] is None:
        raise ValueError("Nu am gasit datele produsului pe pagina. Verifica linkul.")
    date["url"] = url
    return date


MAX_LINKURI = 10


def imparte_linkuri(text):
    """Imparte textul dupa spatii, linii noi, ';' sau ',' (doar inainte de un link).
    Elimina duplicatele, pastrand ordinea."""
    bucati = re.split(r"[\s;]+|,(?=\s*(?:https?://|www\.|emag\.ro))", text or "")
    rezultat = []
    for b in bucati:
        b = b.strip().strip(",")
        if b and b not in rezultat:
            rezultat.append(b)
    return rezultat


def _unul(url):
    try:
        return descarca_produs(url)
    except LinkInvalid as e:
        return {"url": url, "eroare": str(e)}
    except requests.RequestException as e:
        return {"url": url, "eroare": f"Nu am putut accesa pagina: {e}"}
    except ValueError as e:
        return {"url": url, "eroare": str(e)}


def descarca_multiple(text):
    """Intoarce (lista rezultate, mesaj_limita). Fiecare rezultat e un produs sau
    {'url', 'eroare'}. Linkurile se descarca in paralel."""
    linkuri = imparte_linkuri(text)
    mesaj = None
    if len(linkuri) > MAX_LINKURI:
        mesaj = f"Am procesat doar primele {MAX_LINKURI} linkuri din {len(linkuri)}."
        linkuri = linkuri[:MAX_LINKURI]
    if not linkuri:
        return [], mesaj
    with ThreadPoolExecutor(max_workers=5) as pool:
        return list(pool.map(_unul, linkuri)), mesaj
