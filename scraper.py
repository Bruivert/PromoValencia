import yaml
import os
import requests
from adapters.aedas import raspar

def cargar_configuracion():
    with open("config.yml", "r") as archivo:
        return yaml.safe_load(archivo)

def enviar_telegram(mensaje):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("❌ Token o chat ID de Telegram no configurados.")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": mensaje}
        )
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

def main():
    config = cargar_configuracion()
    total_promociones = 0
    promociones_validas = []
    futuras_promociones = []

    for promotora in config["promoters"]:
        nombre = promotora.get("name", "SinNombre")
        url = promotora["url"]
        funcion = promotora.get("adapter")
        try:
            modulo = __import__(f"adapters.{funcion}", fromlist=["raspar"])
            resultados = modulo.raspar(url)
        except Exception as e:
            print(f"[{nombre}] Error técnico en el adaptador: {e}")
            continue

        if resultados is None:
            print(f"[{nombre}] Error técnico, resultados nulos.")
            continue
        if len(resultados) == 0:
            print(f"[{nombre}] Se encontraron 0 promociones.")
        else:
            print(f"[{nombre}] Se encontraron {len(resultados)} promociones.")
        total_promociones += len(resultados)
        for promo in resultados:
            if promo["precio"] <= 270000 and promo["dormitorios"] >= 2:
                promociones_validas.append(promo)
            elif promo["precio"] == 0:
                futuras_promociones.append(promo)

    mensaje = f"🔍 Se analizaron {total_promociones} promociones.\n"
    if promociones_validas:
        mensaje += "✅ Activas:\n"
        for p in promociones_validas:
            mensaje += f"- {p['promocion']} ({p['zona']}): {p['precio']} € – {p['dormitorios']} dorm\n"
    if futuras_promociones:
        mensaje += "📌 Futuras:\n"
        for p in futuras_promociones:
            mensaje += f"- {p['promocion']} ({p['zona']})\n"
    if not promociones_validas and not futuras_promociones:
        mensaje += "❌ Ninguna cumple los criterios."

    print(mensaje)
    enviar_telegram(mensaje)

if __name__ == "__main__":
    main()