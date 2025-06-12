import requests
import json

def raspar(url):
    api_url = "https://api.aedashomes.com/api/v2/developments?filter[province.id]=2509951&page[size]=100"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json',
        'Referer': 'https://www.aedashomes.com/viviendas-obra-nueva?province=2509951'
    }

    promociones_encontradas = []

    try:
        respuesta = requests.get(api_url, headers=headers)
        respuesta.raise_for_status()
        datos = respuesta.json()

        for promo in datos.get('data', []):
            atributos = promo.get('attributes', {})
            nombre_promo = atributos.get('name')
            zona_promo = atributos.get('city')
            precio_texto = atributos.get('price', '0')

            precio_final = 0
            if precio_texto:
                numeros = ''.join(filter(str.isdigit, precio_texto))
                if numeros:
                    if len(numeros) > 2 and numeros.endswith("00"):
                        precio_final = int(numeros[:-2])
                    else:
                        precio_final = int(numeros)

            promociones_encontradas.append({
                'promocion': nombre_promo,
                'zona': zona_promo,
                'precio': precio_final,
                'dormitorios': atributos.get('bedrooms_from', 0),
                'url': f"https://www.aedashomes.com/promociones/{atributos.get('slug')}"
            })

    except requests.exceptions.RequestException as e:
        print(f"[AEDAS] Error técnico al contactar la API: {e}")
    except Exception as e:
        print(f"[AEDAS] Error procesando datos: {e}")

    return promociones_encontradas