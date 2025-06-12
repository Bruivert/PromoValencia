import requests
import os # Necesario para leer las credenciales de forma segura más adelante

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje a un chat de Telegram."""

    # Lee las credenciales de las variables de entorno para mayor seguridad
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Si no se encuentran las credenciales, no se podrá enviar el mensaje
    if not bot_token or not chat_id:
        print("Error: No se han configurado las variables de entorno TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID.")
        return

    # URL de la API de Telegram para enviar mensajes
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
   
    # Parámetros que se enviarán a la API
    params = {
        'chat_id': chat_id,
        'text': mensaje,
        'parse_mode': 'Markdown'  # Permite usar formato como *negrita* o _cursiva_
    }

    try:
        # Realiza la petición a la API de Telegram
        response = requests.post(url, data=params)
        response.raise_for_status() # Lanza un error si la petición no fue exitosa
        print("Mensaje enviado a Telegram con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar el mensaje: {e}")
