import requests
from bs4 import BeautifulSoup

def raspar(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    promociones_encontradas = []

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('.promotion-card')
        for card in cards:
            nombre = card.select_one('.promotion-card__title').get_text(strip=True)
            zona = card.select_one('.promotion-card__location').get_text(strip=True)
            url_promocion = "https://www.aedashomes.com" + card['href'] if card.name == 'a' and card.has_attr('href') else url

            precio_elemento = card.select_one('.promotion-card__price')
            precio = 0
            if precio_elemento:
                texto = precio_elemento.get_text()
                numeros = ''.join(filter(str.isdigit, texto))
                if numeros:
                    precio = int(numeros)

            dormitorios = 0
            if '1 dorm' in card.text:
                dormitorios = 1
            elif '2 dorm' in card.text:
                dormitorios = 2
            elif '3 dorm' in card.text:
                dormitorios = 3
            elif '4 dorm' in card.text:
                dormitorios = 4

            promociones_encontradas.append({
                'promocion': nombre,
                'zona': zona,
                'precio': precio,
                'dormitorios': dormitorios,
                'url': url_promocion
            })

    except Exception as e:
        print(f"Error AEDAS: {e}")

    return promociones_encontradas
