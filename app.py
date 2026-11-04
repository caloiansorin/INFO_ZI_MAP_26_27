import threading
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
import uvicorn
from main import MAX_LINKURI, construieste_date_pagina, curata_linkuri, verifica_lista

# verifica_informatiile scrie numele in variabila globala nume_produs,
# deci facem o singura verificare odata
lacat = threading.Lock()

app = FastAPI()
sabloane = Jinja2Templates(directory=".")


def afiseaza(request, **date):
    return sabloane.TemplateResponse(request, "index.html", construieste_date_pagina(**date))


@app.get("/")
def acasa(request: Request):
    return afiseaza(request)


@app.get("/verifica")
def verifica(request: Request, link: list[str] = Query(default=[])):
    linkuri = curata_linkuri(link)
    if not linkuri:
        return afiseaza(request, aviz="Adaugă cel puțin un link de pe emag.ro.")
    aviz = None
    if len(linkuri) > MAX_LINKURI:
        aviz = f"Am verificat doar primele {MAX_LINKURI} din cele {len(linkuri)} linkuri primite."
        linkuri = linkuri[:MAX_LINKURI]
    with lacat:
        produse = verifica_lista(linkuri)
    return afiseaza(request, produse=produse, linkuri=linkuri, aviz=aviz)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
