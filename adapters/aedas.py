import requests
from bs4 import BeautifulSoup

def scrape(url):
    promos = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select(".promocion")
        for card in cards:
            nombre = card.select_one(".titulo").get_text(strip=True)
            ubicacion = card.select_one(".localidad").get_text(strip=True).lower()
            link = card.select_one("a")["href"]
            precio_elem = card.select_one(".precio")

            if not precio_elem:
                continue  # no tiene precio, salta

            precio_txt = precio_elem.get_text(strip=True).replace(".", "").replace("€", "").replace(",", "")
            try:
                precio = int(precio_txt)
            except:
                continue

            dorm_elem = card.select_one(".iconos li:nth-of-type(2)")
            if dorm_elem:
                try:
                    dormitorios = int(dorm_elem.get_text(strip=True)[0])
                except:
                    dormitorios = 0
            else:
                dormitorios = 0

            promos.append({
                "nombre": nombre,
                "zona": ubicacion,
                "precio": precio,
                "dormitorios": dormitorios,
                "url": link
            })

    except Exception as e:
        print("Error AEDAS:", e)

    return promos
