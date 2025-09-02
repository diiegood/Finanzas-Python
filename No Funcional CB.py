import os
import requests
from bs4 import BeautifulSoup

try:
    import cloudscraper
    session = cloudscraper.create_scraper()
    print("> Usando cloudscraper")
except ImportError:
    print("> Aviso: cloudscraper no disponible. Usando requests.Session()")
    session = requests.Session()


def debug_guardar_html(resp, categoria, isin):
    """Guarda el contenido HTML de una respuesta para depuración."""
    carpeta_debug = "cbonds_debug"
    os.makedirs(carpeta_debug, exist_ok=True)
    filename = f"{carpeta_debug}/debug_cbonds_{categoria}_{isin}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print(f"[*] HTML guardado en: {filename}")


def obtener_moneda_tabla(soup, ticker_buscado):
    """
    Busca en la tabla de cotizaciones una coincidencia exacta del ticker 
    y devuelve la moneda de esa fila.
    """
    # --- ESTE ES EL CAMBIO CLAVE ---
    # Usamos un selector más específico para apuntar a la tabla con datos y no a la oculta.
    tabla = soup.select_one("div.table_wrapper table.full")
    
    if not tabla:
        print("    > DEBUG: La tabla de datos ('div.table_wrapper table.full') NO fue encontrada.")
        return None
    
    filas = tabla.select("tbody tr")
    if not filas:
        print("    > DEBUG: No se encontraron filas (<tr>) en el <tbody> de la tabla.")
        return None

    print(f"    > DEBUG: Tabla encontrada con {len(filas)} filas. Analizando...")

    for i, fila in enumerate(filas):
        td_ticker = fila.select_one("td.field_tiker")
        # Selector robusto para la moneda
        td_currency = fila.select_one("td.field_currency, td.field_currency_name")

        if td_ticker and td_currency:
            ticker = td_ticker.get_text(strip=True)
            # Imprimimos lo que encontramos para asegurarnos de que la comparación es correcta
            # print(f"    > DEBUG: Fila {i+1} -> Ticker encontrado: '{ticker}'")

            if ticker == ticker_buscado:
                currency = td_currency.get_text(strip=True)
                print(f"    > ¡Éxito! Coincidencia exacta encontrada en la fila {i+1}: Ticker='{ticker}', Moneda='{currency}'")
                return currency

    return None


def obtener_datos_cbonds(isin, ticker_objetivo):
    """
    Recorre las categorías de cbonds, valida el encabezado y extrae la moneda.
    """
    categorias = ["stocks", "bonds", "indexes", "company", "etf"]
    resultado = {
        "isin": isin,
        "ticker": ticker_objetivo,
        "url": None,
        "moneda": None,
        "motivo": None
    }

    for categoria in categorias:
        url = f"https://cbonds.com/{categoria}/{isin}/"
        try:
            resp = session.get(url, timeout=20)
            print(f"  > Intentando categoría: {categoria} -> {url} | Status: {resp.status_code}")

            if resp.status_code == 200:
                debug_guardar_html(resp, categoria, isin)
                soup = BeautifulSoup(resp.text, "lxml")

                h1 = soup.select_one("h1#cb_stock_ttl")
                if not h1:
                    continue
                
                encabezado = h1.get_text(" ", strip=True)
                if isin not in encabezado or ticker_objetivo not in encabezado:
                    print("    > El encabezado no contiene ISIN o ticker esperado.")
                    continue
                
                print("    > Encabezado validado con ISIN y Ticker correctos.")
                
                moneda = obtener_moneda_tabla(soup, ticker_objetivo)
                if moneda:
                    resultado["url"] = url
                    resultado["moneda"] = moneda
                    resultado["motivo"] = "OK"
                    return resultado
                else:
                    print(f"    > No se encontró una fila con el ticker exacto '{ticker_objetivo}'")

            elif resp.status_code == 404:
                print("    > Página no encontrada (404)")

        except requests.exceptions.RequestException as e:
            print(f"    > Error al conectar: {e}")

    if not resultado["moneda"]:
        resultado["motivo"] = "No se encontró moneda (búsqueda finalizada sin éxito)"

    return resultado


if __name__ == "__main__":
    isin_test = "US8965221091"
    ticker_test = "TRN"

    print("\n--- PRUEBA DE SCRAPING CBONDS ---")
    resultado = obtener_datos_cbonds(isin_test, ticker_test)

    print("\n--- RESULTADOS ---")
    for k, v in resultado.items():
        print(f"{k}: {v}")
    print("-------------------")