import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import time
import random
import math
import os
os.chdir('S:/Edward Files/Programa ISIN')
print(f"Directorio de trabajo actual: {os.getcwd()}")


# -------------------------------
# Configuración general
# -------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

BASE_MS = "https://www.marketscreener.com"

# Parámetros de IO
EXCEL_INPUT_PATH = "ISINs Faltantes.xlsx"    # <-- tu archivo
EXCEL_SHEET = "Hoja2"                       # <-- tu hoja
EXCEL_OUTPUT_PATH = "Resultados ISIN.xlsx"

# Tamaño del lote
BATCH_SIZE = 20

# -------------------------------
# Utilidad de red
# -------------------------------
def fetch(url, params=None, headers=HEADERS, timeout=20):
    """GET con retry simple (fallback verify=False). Devuelve (response, error_str)."""
    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r, None
    except requests.exceptions.RequestException:
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout, verify=False)
            r.raise_for_status()
            return r, None
        except requests.exceptions.RequestException as e:
            # Devuelve un error un poco más específico
            return None, f"Error request: {type(e).__name__}"

# -------------------------------
# MarketScreener: búsqueda por ISIN, elección por emisora (ticker)
# -------------------------------
def ms_search_url_by_isin_and_ticker(isin: str, emisora: str):
    """
    Busca en MarketScreener con q=ISIN y selecciona la fila cuyo TICKER (emisora)
    coincide exactamente con 'emisora'. Devuelve (url_ms, reason_or_None).
    """
    if not emisora or (isinstance(emisora, float) and math.isnan(emisora)):
        return None, "Emisora vacía"

    search_url = f"{BASE_MS}/search/"
    r, err = fetch(search_url, params={"q": isin})
    if err:
        return None, f"{err}"

    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tbody tr")
    if not rows:
        return None, "No encontrado"

    # En cada fila, buscamos:
    # - enlace a ficha (nombre): a.link.link--blue[href^="/quote/"]
    # - celda de ticker: td.table-child--w80 (según tu outerHTML)
    for tr in rows:
        link_tag = tr.select_one('a.link.link--blue[href^="/quote/"]')
        if not link_tag:
            continue

        ticker_cell = None
        for td in tr.find_all("td"):
            classes = td.get("class", [])
            if "table-child--w80" in classes:
                ticker_cell = td
                break

        if not ticker_cell:
            continue

        ticker = ticker_cell.get_text(strip=True).upper()
        if ticker == str(emisora).upper():
            href = link_tag.get("href", "")
            if href:
                return BASE_MS + href, None

    return None, "No coincide emisora"

def ms_currency_and_verify(url_ms: str, expected_isin: str):
    """
    Verifica que el ISIN en la ficha coincida exactamente y extrae la moneda
    del precio en tiempo real. Devuelve (currency_or_NA, url, reason_or_None).
    """
    if not url_ms:
        # Este caso ya no debería ocurrir por la nueva lógica, pero se mantiene por seguridad.
        return "N/A", None, "URL vacía"

    r, err = fetch(url_ms)
    if err:
        return "N/A", url_ms, f"{err}"

    soup = BeautifulSoup(r.text, "html.parser")

    # Verificación estricta de ISIN: debe aparecer EXACTO en el texto
    page_text = soup.get_text(" ", strip=True)
    if expected_isin not in page_text:
        return "N/A", url_ms, "No coincide ISIN"

    # Extraer la moneda (varios selectores por robustez)
    selectors = [
        "td.is__realtime-last sup span",    # observado
        'span[itemprop="priceCurrency"]',   # semántico
        ".is__realtime-character sup",      # Otra posible ubicación
        "sup span"                          # fallback
    ]
    currency = None
    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            curr = el.get_text(strip=True)
            if curr and len(curr) <= 6:  # USD, EUR, BRL, etc.
                currency = curr
                break

    if currency:
        return currency, url_ms, None
    else:
        return "N/A", url_ms, "Moneda no encontrada"

# -------------------------------
# DivvyDiary: verificación (ISIN + emisora) y Dividend Currency
# -------------------------------
def divvydiary_currency_and_verify(isin: str, emisora: str):
    """
    Abre https://divvydiary.com/en/{isin}, verifica ISIN y emisora en encabezados,
    y extrae 'Dividend Currency'. Devuelve (currency_or_NA, url, reason_or_None).
    """
    url_divvy = f"https://divvydiary.com/en/{isin}"
    r, err = fetch(url_divvy)
    if err:
        return "N/A", url_divvy, f"{err}"

    soup = BeautifulSoup(r.text, "html.parser")

    # Verificar ISIN exacto en la página
    if isin not in soup.get_text(" ", strip=True):
        return "N/A", url_divvy, "No coincide ISIN"

    # Verificar emisora (ticker) en encabezados y título
    header_texts = []
    for tag in soup.select("h1, h2, header, .instrument-header, .stock-header"):
        header_texts.append(tag.get_text(" ", strip=True))
    if soup.title and soup.title.string:
        header_texts.append(soup.title.string)

    header_blob = " ".join(header_texts).upper()
    if str(emisora).upper() not in header_blob:
        return "N/A", url_divvy, "No coincide emisora"

    # Buscar 'Dividend Currency'
    dt = soup.find("dt", string=lambda s: isinstance(s, str) and s.strip().lower() == "dividend currency")
    if dt:
        dd = dt.find_next("dd")
        if dd:
            return dd.get_text(strip=True), url_divvy, None

    return "N/A", url_divvy, "Moneda no encontrada"

# -------------------------------
# Lectura de Excel (robusta a mayúsculas)
# -------------------------------
def load_isins_from_excel(path: str, sheet_name: str):
    """Carga ISINs y Emisoras desde un archivo Excel."""
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{path}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return None

    df.columns = df.columns.str.strip().str.upper()
    col_isin = None
    for c in ["ISIN"]:
        if c in df.columns:
            col_isin = c
            break
    col_emisora = None
    for c in ["EMISORA", "TICKER", "EMISOR", "SYMBOL"]:
        if c in df.columns:
            col_emisora = c
            break
    if col_isin is None or col_emisora is None:
        raise ValueError("No se encontraron columnas 'ISIN' y 'EMISORA' (o equivalente) en el Excel.")
    
    df = df[[col_isin, col_emisora]].copy()
    df.rename(columns={col_isin: "ISIN", col_emisora: "EMISORA"}, inplace=True)
    
    df["ISIN"] = df["ISIN"].astype(str).str.strip()
    df["EMISORA"] = df["EMISORA"].astype(str).str.strip()
    df.dropna(subset=["ISIN", "EMISORA"], inplace=True)
    df = df[df["ISIN"].str.len() > 5] # Filtro básico para ISINs inválidos
    return df

# -------------------------------
# Proceso por lotes (VERSIÓN CORREGIDA)
# -------------------------------
def procesar_lotes(df_pairs: pd.DataFrame):
    """Procesa un DataFrame de pares ISIN/Emisora en lotes."""
    results = []
    total = len(df_pairs)
    if total == 0:
        print("No hay pares ISIN/Emisora para procesar.")
        return pd.DataFrame()

    num_batches = math.ceil(total / BATCH_SIZE)

    for idx in range(0, total, BATCH_SIZE):
        batch = df_pairs.iloc[idx: idx + BATCH_SIZE]
        print(f"\nProcesando lote {(idx // BATCH_SIZE) + 1} de {num_batches}: {len(batch)} ISINs")

        for j, row in batch.iterrows():
            isin = row["ISIN"]
            emisora = row["EMISORA"]

            # --- Lógica de MarketScreener corregida ---
            currency_ms = "N/A"
            url_ms_final = None
            fail_ms = None

            # Paso 1: Intentar buscar la URL
            url_ms_search, fail_ms_search = ms_search_url_by_isin_and_ticker(isin, emisora)

            # Paso 2: Solo si la búsqueda fue exitosa, proceder a verificar y extraer detalles
            if fail_ms_search:
                # Si la búsqueda falló, ese es nuestro error final para MS.
                fail_ms = fail_ms_search
            else:
                # Si la búsqueda tuvo éxito (url_ms_search no es None), ahora obtenemos los detalles.
                currency_ms, url_ms_final, fail_ms_detail = ms_currency_and_verify(url_ms_search, isin)
                if fail_ms_detail:
                    # Si la extracción de detalles falló, ese es el error.
                    fail_ms = fail_ms_detail
                # Si no hubo fail_ms_detail, fail_ms permanece como None (éxito).

            # Si la URL se encontró pero el detalle falló, aún queremos registrar la URL.
            if not url_ms_final and url_ms_search:
                url_ms_final = url_ms_search

            # --- Lógica de DivvyDiary (sin cambios) ---
            currency_dd, url_dd, fail_dd = divvydiary_currency_and_verify(isin, emisora)

            results.append({
                "ISIN": isin,
                "Emisora": emisora,
                "URL_MS": url_ms_final,
                "Currency_MS": currency_ms,
                "Fail_MS": fail_ms, # Usamos la variable consolidada 'fail_ms'
                "URL_Divvy": url_dd,
                "Currency_Divvy": currency_dd,
                "Fail_Divvy": fail_dd
            })
            
            MS = results[j]["Currency_MS"]
            DD = results[j]["Currency_Divvy"]
            print(f"  - ISIN: {isin} | Emisora: {emisora} | MS: {MS} | DD: {DD}")

            # Pausa entre ISINs
            time.sleep(1 + random.random())

        # Pausa entre lotes (si no es el último lote)
        if idx + BATCH_SIZE < total:
            pause_time = 2 + random.random()
            print(f"  Pausa de {pause_time:.2f} segundos antes del siguiente lote...")
            time.sleep(pause_time)

    return pd.DataFrame(results)

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    df_pairs = load_isins_from_excel(EXCEL_INPUT_PATH, EXCEL_SHEET)
    
    if df_pairs is not None:
        print(f"Se encontraron {len(df_pairs)} pares ISIN/Emisora para procesar.")
        df_results = procesar_lotes(df_pairs)

        if not df_results.empty:
            # Guardar
            df_results.to_excel(EXCEL_OUTPUT_PATH, index=False)

            # Resumen rápido
            num_success_ms = (df_results["Currency_MS"] != "N/A").sum()
            num_success_dd = (df_results["Currency_Divvy"] != "N/A").sum()
            num_success = ((df_results["Currency_MS"] != "N/A") | (df_results["Currency_Divvy"] != "N/A")).sum()
            print("\n--- RESUMEN ---")
            print(f"Resultados guardados en: {EXCEL_OUTPUT_PATH}")
            print(f"Total procesados: {len(df_results)}")
            print(f"Éxitos MarketScreener: {num_success_ms} ({num_success_ms/len(df_results):.1%})")
            print(f"Éxitos DivvyDiary: {num_success_dd} ({num_success_dd/len(df_results):.1%})")
            print(f"Éxitos Conjuntos: {num_success} ({num_success/len(df_results):.1%})")
            print("\nAnálisis de fallos en MarketScreener:")
            print(df_results["Fail_MS"].value_counts().to_string())
            print("\nAnálisis de fallos en DivvyDiary:")
            print(df_results["Fail_Divvy"].value_counts().to_string())
            print("\n-----------------")