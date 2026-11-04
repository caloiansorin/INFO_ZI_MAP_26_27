import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36",
    "Accept-Language": "ro-RO,ro;q=0.9,en;q=0.8",
}


# Descarcă pagina și o transformă într-un obiect ușor de analizat.
def fetch_page(url):
    parsed_url = urlparse(url.strip())
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise requests.RequestException(
            "Introdu un URL valid, cu http:// sau https://."
        )

    response = requests.get(url, headers=REQUEST_HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


# Returnează primul text găsit folosind lista de selectori CSS.
def first_text(page, selectors):
    for selector in selectors:
        element = page.select_one(selector)
        if element:
            text = element.get_text(" ", strip=True)
            if text:
                return text
    return ""


def structured_price(page):
    def find_offer_price(value):
        if isinstance(value, dict):
            offers = value.get("offers")
            if isinstance(offers, dict) and offers.get("price") is not None:
                return str(offers["price"])
            if isinstance(offers, list):
                for offer in offers:
                    if isinstance(offer, dict) and offer.get("price") is not None:
                        return str(offer["price"])
            for child in value.values():
                result = find_offer_price(child)
                if result:
                    return result
        elif isinstance(value, list):
            for child in value:
                result = find_offer_price(child)
                if result:
                    return result
        return ""

    for script in page.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(script.string or script.get_text())
        except json.JSONDecodeError:
            continue
        price = find_offer_price(data)
        if price:
            return price

    for selector in [
        'meta[itemprop="price"]',
        'meta[property="product:price:amount"]',
    ]:
        element = page.select_one(selector)
        if element and element.get("content"):
            return element["content"]
    return ""


# Construiește un dicționar doar cu numele și prețul produsului.
def get_product_details(url):
    page = fetch_page(url)
    return {
        "titlu": first_text(page, ["h1.page-title", "h1"]),
        "pret": structured_price(page),
    }


# Extrage prețul și numele produsului pentru pagina de monitorizare.
def get_price_and_name(url):
    product = get_product_details(url)
    if not product["pret"]:
        raise requests.RequestException("Prețul nu a fost găsit pe pagină.")

    return product["pret"], product["titlu"]
