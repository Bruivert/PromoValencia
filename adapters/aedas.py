import requests

def scrape(url):
    promos = []
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "pagination": {"page": 1, "size": 100},
            "filters": {
                "provinceIds": [2509951]  # ID de Valencia
            }
        }

        response = requests.post("https://api.aedashomes.com/api/product/public/search", json=payload, headers=headers, timeout=10)
        data = response.json()

        for item in data.get("items", []):
            nombre = item.get("name", "")
            ubicacion = item.get("municipality", "").lower()
            precio = item.get("price", 0)
            dormitorios = item.get("bedrooms", 0)
            link = f'https://www.aedashomes.com{item.get("seoUrl", "")}'

            promos.append({
                "nombre": nombre,
                "zona": ubicacion,
                "precio": int(precio),
                "dormitorios": int(dormitorios),
                "url": link
            })

    except Exception as e:
        print("Error AEDAS:", e)

    return promos
