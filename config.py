import os

from dotenv import load_dotenv

# Încarcă valorile configurate în fișierul .env.
load_dotenv()

PRODUCT_URL = os.getenv(
    "PRODUCT_URL",
    "https://www.emag.ro/memorie-ram-g-skill-96gb-ddr5-5600mhz-f5-5600j4040d48gx2-rs5k/pd/DGNTTTYBM/",
)
DATABASE_PATH = os.getenv("ADRESA_DB", "preturi.db")
EMAIL_SENDER = os.getenv("EMAIL_EXPEDITOR")
EMAIL_PASSWORD = os.getenv("APP_PASSWORD")
HOST = "127.0.0.1"
PORT = 8000
