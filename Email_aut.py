
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from email.utils import formataddr
from datetime import datetime
from zoneinfo import ZoneInfo
from babel.dates import format_datetime


load_dotenv(override=True)

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]

SMTP_HOST = os.environ.get("SMTP_HOST", "in-v3.mailjet.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ["SMTP_USER"]   # Mailjet API Key
SMTP_PASS = os.environ["SMTP_PASS"]   # Mailjet Secret Key

# Cargar HTML
with open("template/email.html", "r", encoding="utf-8") as f:
    html_body = f.read()



now = datetime.now(ZoneInfo("America/Santiago"))
fecha_hoy = "Hoy, " + format_datetime(now, "EEEE d 'de' MMMM 'de' y", locale="es").capitalize()



# Reemplazar placeholder
html_body = html_body.replace("{{FECHA}}", fecha_hoy)

msg = EmailMessage()
msg["Subject"] = "Buenos días, que tengas un hermoso día 💖"

msg["From"] = formataddr(("Mensaje de buenos días", EMAIL_FROM))
msg["Reply-To"] = EMAIL_FROM

msg["To"] = EMAIL_TO

msg.set_content("Tu cliente de correo no soporta HTML.")
msg.add_alternative(html_body, subtype="html")

with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(SMTP_USER, SMTP_PASS)
    smtp.send_message(msg)

print("✅ Email enviado con Mailjet")

