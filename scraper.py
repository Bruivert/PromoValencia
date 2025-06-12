import os
import yaml
import importlib
import requests

MIN_PRICE = 0
MAX_PRICE = 270000
MIN_ROOMS = 2
ZONAS = ["valencia", "Quart de Poblet", "Manises", "Paterna", "Mislata"]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def filtrar(promo):
    if promo["precio"] > MAX_PRICE:
        return False
    if promo["dormitorios"] < MIN_ROOMS:
        return False
    if not any(z in promo["zona"].lower() for z in ZONAS):
        return False
    return True

def main():
    with open("config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    promociones = []
    total_detectadas = 0

    for prom in config["promoters"]:
        try:
            adapter = importlib.import_module(f"adapters.{prom['adapter']}")
            resultados = adapter.scrape(prom["url"])
            total_detectadas += len(resultados)
            for r in resultados:
                if filtrar(r):
                    promociones.append(r)
        except Exception as e:
            print(f"Error en {prom['name']}: {e}")

    if not promociones:
        send_telegram(f"🔍 Se analizaron {total_detectadas} promociones.\n❌ Ninguna cumple los criterios.")
    else:
        send_telegram(f"🔍 Se analizaron {total_detectadas} promociones.\n✅ {len(promociones)} cumplen los criterios.")
        for p in promociones:
            msg = (
                f"<b>{p['nombre']}</b>\n"
                f"Zona: {p['zona']}\n"
                f"Precio: {p['precio']} €\n"
                f"Dormitorios: {p['dormitorios']}\n"
                f"<a href='{p['url']}'>Ver promoción</a>"
            )
            send_telegram(msg)

if __name__ == "__main__":
    main()
