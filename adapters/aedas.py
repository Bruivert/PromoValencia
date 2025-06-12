import requests
from bs4 import BeautifulSoup

def raspar(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    promociones_encontradas = []

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        cards = soup.select('article.card-promotion')  # Selector actualizado

        for card in cards:
            nombre = card.select_one('.card-title').get_text(strip=True)
            zona = card.select_one('.card-location').get_text(strip=True)
            precio_elemento = card.select_one('.card-price')
            precio = 0
            if precio_elemento:
                texto = precio_elemento.get_text()
                numeros = ''.join(filter(str.isdigit, texto))
                if numeros:
                    precio = int(numeros)

            dormitorios = 0
            info_text = card.get_text()
            if '1 dormitorio' in info_text:
                dormitorios = 1
            elif '2 dormitorios' in info_text:
                dormitorios = 2
            elif '3 dormitorios' in info_text:
                dormitorios = 3
            elif '4 dormitorios' in info_text:
                dormitorios = 4

            href = card.select_one('a')
            url_promocion = f"https://www.aedashomes.com{href['href']}" if href and href.has_attr('href') else url

            promociones_encontradas.append({
                'promocion': nombre,
                'zona': zona,
                'precio': precio,
                'dormitorios': dormitorios,
                'url': url_promocion
            })

    except Exception as e:
        print(f"[AEDAS] Error: {e}")

    print(f"[AEDAS] Se encontraron {len(promociones_encontradas)} promociones.")
    return promociones_encontradas
