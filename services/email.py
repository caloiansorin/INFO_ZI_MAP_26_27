import smtplib
from email.mime.text import MIMEText

from config import EMAIL_PASSWORD, EMAIL_SENDER


# Trimite un email simplu prin serverul securizat Gmail.
def send_email(recipient, subject, content):
    # Fără aceste valori, autentificarea la serverul de email nu este posibilă.
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        raise ValueError("Configura EMAIL_EXPEDITOR și APP_PASSWORD în fișierul .env.")

    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = EMAIL_SENDER
    message["To"] = recipient

    # Conexiunea SSL protejează autentificarea și transmiterea mesajului.
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(EMAIL_SENDER, EMAIL_PASSWORD)
        email.sendmail(EMAIL_SENDER, recipient, message.as_string())
