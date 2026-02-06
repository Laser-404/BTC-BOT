import requests
import smtplib
from email.mime.text import MIMEText
import os

# ========================
# TWOJE DANE
# ========================

btc_amount = 0.00049

gmail = "magik.narodowy@gmail.com"
import os
haslo = os.environ["EMAIL_PASSWORD"]


# ========================
# POBRANIE CENY BTC
# ========================

url = "https://api.coinbase.com/v2/prices/BTC-EUR/spot"
response = requests.get(url)
data = response.json()
btc_price = float(data["data"]["amount"])


current_value = btc_amount * btc_price

# ========================
# HISTORIA CEN
# ========================

history_file = "btc_history.txt"

prices = []

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        prices = [float(line.strip()) for line in f.readlines()]

# dodaj dzisiejszą cenę
prices.append(btc_price)

# zapisz historię
with open(history_file, "w") as f:
    for p in prices[-7:]:  # trzymamy tylko 7 dni
        f.write(str(p) + "\n")

# ========================
# PROCENT DZIENNY
# ========================

daily_change = 0
if len(prices) > 1:
    yesterday = prices[-2]
    daily_change = ((btc_price - yesterday) / yesterday) * 100

# ========================
# PROCENT TYGODNIOWY
# ========================

weekly_change = 0
if len(prices) >= 7:
    week_ago = prices[0]
    weekly_change = ((btc_price - week_ago) / week_ago) * 100

# ========================
# EMOJI TREND
# ========================

if daily_change > 3:
    trend = "🚀 BTC mocno rośnie"
elif daily_change > 0:
    trend = "📈 BTC rośnie"
elif daily_change < -3:
    trend = "💥 BTC mocno spada"
elif daily_change < 0:
    trend = "📉 BTC spada"
else:
    trend = "➖ Bez zmian"

# ========================
# MAIL
# ========================

subject = "BTC Daily Report"

body = f"""
BTC RAPORT

Cena BTC: {btc_price:.2f} €
Twoje BTC: {btc_amount}
Wartość: {current_value:.2f} €

Zmiana 24h: {daily_change:.2f} %
Zmiana 7 dni: {weekly_change:.2f} %

{trend}
"""

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = gmail
msg["To"] = gmail

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(gmail, haslo)
    server.send_message(msg)

print("Mail wysłany!")

