import requests
from bs4 import BeautifulSoup

def raspar(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    promociones_encontradas = []

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('.promotion-card')
        print(f"[AEDAS] Se encontraron {len(cards)} tarjetas de promoción en la página.")

        for card in cards:
            nombre = card.select_one('.promotion-card__title')
            zona = card.select_one('.promotion-card__location')
            precio_elemento = card.select_one('.promotion-card__price')
            url_promocion = "https://www.aedashomes.com" + card['href'] if card.name == 'a' and card.has_attr('href') else ""

            if not (nombre and zona and precio_elemento):
                continue  # Saltar tarjetas incompletas

            nombre = nombre.get_text(strip=True)
            zona = zona.get_text(strip=True)

            texto_precio = precio_elemento.get_text()
            numeros = ''.join(filter(str.isdigit, texto_precio))
            precio = int(numeros) if numeros else 0

            dormitorios = 0
            card_text = card.text
            if '1 dorm' in card_text:
                dormitorios = 1
            elif '2 dorm' in card_text:
                dormitorios = 2
            elif '3 dorm' in card_text:
                dormitorios = 3
            elif '4 dorm' in card_text:
                dormitorios = 4

            promociones_encontradas.append({
                'promocion': nombre,
                'zona': zona,
                'precio': precio,
                'dormitorios': dormitorios,
                'url': url_promocion
            })

        print(f"[AEDAS] Promociones válidas encontradas: {len(promociones_encontradas)}")

    except Exception as e:
        print(f"[AEDAS][ERROR] {e}")

    return promociones_encontradas
