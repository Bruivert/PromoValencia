import requests
from bs4 import BeautifulSoup

def raspar(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    promociones = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.select("div.card.card-product")  # Selector CSS de promociones

        for card in cards:
            nombre = card.select_one("h2.product-title")
            zona = card.select_one("span.product-location")
            precio = card.select_one("span.product-price")
            enlace = card.select_one("a[href]")

            nombre_texto = nombre.get_text(strip=True) if nombre else "Sin nombre"
            zona_texto = zona.get_text(strip=True) if zona else "Sin zona"
            precio_texto = precio.get_text(strip=True).replace(".", "").replace("€", "").replace("Desde", "").strip() if precio else "0"
            url_texto = "https://www.aedashomes.com" + enlace['href'] if enlace else url

            try:
                precio_final = int(''.join(filter(str.isdigit, precio_texto)))
            except:
                precio_final = 0

            promociones.append({
                'promocion': nombre_texto,
                'zona': zona_texto,
                'precio': precio_final,
                'dormitorios': 0,
                'url': url_texto
            })

    except Exception as e:
        print(f"[AEDAS] Error: {e}")

    return promociones
