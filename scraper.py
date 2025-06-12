
import yaml
from adapters.aedas import raspar

def cargar_configuracion():
    with open("config.yml", "r") as archivo:
        return yaml.safe_load(archivo)

def main():
    config = cargar_configuracion()
    total_promociones = 0
    promociones_validas = []
    futuras_promociones = []

    for promotora in config["promoters"]:
        nombre = promotora.get("name", "SinNombre")
        url = promotora["url"]
        funcion = promotora["funcion"]
        modulo = __import__(f"adapters.{funcion}", fromlist=["raspar"])
        resultados = modulo.raspar(url)

        total_promociones += len(resultados)
        for promo in resultados:
            if promo["precio"] <= 270000 and promo["dormitorios"] >= 2:
                promociones_validas.append(promo)
            elif promo["precio"] == 0:
                futuras_promociones.append(promo)

    print(f"🔍 Se analizaron {total_promociones} promociones.")
    if promociones_validas:
        print("✅ Activas:")
        for p in promociones_validas:
            print(f"- {p['promocion']} ({p['zona']}): {p['precio']} € – {p['dormitorios']} dorm")
    if futuras_promociones:
        print("📌 Futuras:")
        for p in futuras_promociones:
            print(f"- {p['promocion']} ({p['zona']})")

if __name__ == "__main__":
    main()
