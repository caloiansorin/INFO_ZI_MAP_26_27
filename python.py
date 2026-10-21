#Acesta este fisierul meu facut in timpul orei, dar nu are si fisierul .html cu interfata site-ului deoarece nu folosesc AI
#si am decis sa dau push in branch-ul meu cu proiectul din main
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}