import requests
import json

def scrape(url):
    api_url = "https://api.aedashomes.com/api/v2/developments?filter[province.id]=2509951&page[size]=100"

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    promociones_encontradas = []

    try:
        respuesta = requests.get(api_url, headers=headers)
        respuesta.raise_for_status()
        datos = respuesta.json()

        for promo in datos.get('data', []):
            atributos = promo.get('attributes', {})

            nombre = atributos.get('name', 'Sin nombre')
            zona = atributos.get('city', 'Sin zona')
            precio_texto = atributos.get('price', '')
            dormitorios = atributos.get('bedrooms_from', 0)
            slug = atributos.get('slug', '')

            precio = 0
            if precio_texto:
                numeros = ''.join(filter(str.isdigit, precio_texto))
                if len(numeros) > 2 and numeros.endswith("00"):
                    precio = int(numeros[:-2])
                elif numeros:
                    precio = int(numeros)

            promociones_encontradas.append({
                'promocion': nombre,
                'zona': zona,
                'precio': precio,
                'dormitorios': dormitorios,
                'url': f"https://www.aedashomes.com/promociones/{slug}"
            })

    except requests.exceptions.RequestException as e:
        print(f"❌ Error conexión AEDAS: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error parsing AEDAS JSON: {e}")

    return promociones_encontradas
