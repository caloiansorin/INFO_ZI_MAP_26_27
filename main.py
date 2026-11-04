import datetime
from urllib.parse import parse_qs

import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from config import HOST, PORT, PRODUCT_URL
from database import get_price_history, get_price_statistics
from scraper import get_price_and_name

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Funcție comună pentru afișarea unui template HTML.
def render_template(request, template_name, context=None, status_code=200):
    return templates.TemplateResponse(
        request=request,
        name=template_name,
        context=context or {},
        status_code=status_code,
    )


# Adună toate datele necesare pentru pagina principală.
def get_home_context():
    current_price, product_name = get_price_and_name(PRODUCT_URL)
    minimum_price, maximum_price, checks = get_price_statistics()
    return {
        "nume_produs": product_name,
        "pret_actual": current_price,
        "timestamp": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "url_produs": PRODUCT_URL,
        "pret_minim": minimum_price,
        "pret_maxim": maximum_price,
        "numar_verificari": checks,
        "continut_db": get_price_history(),
    }


@app.get("/")
def home(request: Request):
    # Pagina principală afișează prețul actual și istoricul verificărilor.
    return render_template(request, "index.html", get_home_context())


@app.get("/index2.html")
def index2(request: Request):
    return render_template(request, "index2.html")

@app.get("/index3.html")
def index3(request: Request):
    return render_template(request, "index3.html")

@app.post("/index2.html")
async def index2_submit(request: Request):
    # Citește linkul introdus de utilizator în formular.
    body = await request.body()
    form_data = parse_qs(body.decode("utf-8"))
    link = form_data.get("link", [""])[0]

    try:
        # Descarcă și extrage doar numele și prețul produsului.
        price, product_name = get_price_and_name(link)
    except requests.RequestException as error:
        # Afișează o eroare prietenoasă dacă pagina nu poate fi accesată.
        return render_template(
            request,
            "index2.html",
            {"eroare": f"Nu am putut accesa pagina: {error}"},
            status_code=502,
        )

    return render_template(
        request,
        "index2.html",
        {"titlu": product_name, "pret": price, "link": link},
    )


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
