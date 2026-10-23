import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"
ORAS_IMPLICIT = "Băicoi"


@asynccontextmanager
async def lifespan(app: FastAPI):
  app.state.client = httpx.AsyncClient(timeout=5.0)
  yield
  await app.state.client.aclose()


app = FastAPI(lifespan=lifespan)
app.mount("/src", StaticFiles(directory="src"), name="src")


@app.get("/")
async def home():
  return FileResponse("src/index.html")


@app.get("/mesaj")
async def mesaj(request: Request, oras: str = ORAS_IMPLICIT):
  params = {"q": oras, "appid": API_KEY, "units": "metric", "lang": "ro"}

  try:
    resp = await request.app.state.client.get(URL_WEATHER, params=params)
  except httpx.RequestError:
    raise HTTPException(
        status_code=504, detail="Serviciul meteo nu a răspuns la timp."
    )

  if resp.status_code == 404:
    raise HTTPException(status_code=404, detail="Orașul nu a putut fi găsit.")
  if resp.status_code != 200:
    raise HTTPException(status_code=502, detail="Eroare la serviciul meteo.")

  data = resp.json()
  return {
    "oras": data["name"],
    "starea_vremii": data["weather"][0]["description"].capitalize(),
    "temperatura": round(data["main"]["temp"]),
    "viteza_vant": round(data["wind"]["speed"] * 3.6, 1),
    "iconita": data["weather"][0]["icon"],
  }