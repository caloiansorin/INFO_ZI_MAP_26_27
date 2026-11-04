import datetime
import sqlite3

from config import DATABASE_PATH


# Deschide baza de date și creează tabelul dacă nu există.
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS pret (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pret INTEGER NOT NULL,
            data_verificare TEXT NOT NULL
        )
        """
    )
    return connection


# Salvează o nouă verificare de preț împreună cu data și ora.
def save_price(price):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO pret (pret, data_verificare)
            VALUES (?, ?)
            """,
            (price, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        )


# Returnează toate verificările într-un format potrivit pentru template.
def get_price_history():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute("SELECT * FROM pret").fetchall()
    return [dict(row) for row in rows]


# Calculează prețul minim, maxim și numărul total de verificări.
def get_price_statistics():
    with get_connection() as connection:
        result = connection.execute(
            "SELECT MIN(pret), MAX(pret), COUNT(pret) FROM pret"
        ).fetchone()
    return result[0], result[1], result[2]
