import os
import sys
import time
import random
import math
import urllib3
from typing import Optional, Dict, Tuple

import requests
import pandas as pd
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# Ajusta según tu entorno
# ---------------------------------------------------------
os.chdir('S:/Edward Files/Programa ISIN')
print(f"Directorio de trabajo actual: {os.getcwd()}")

INPUT_FILE = "ISINs Faltantes.xlsx"
INPUT_SHEET = "Hoja4"
OUTPUT_FILE = "Resultados_CBonds.xlsx"

# Batch / pausas (rangos para random.uniform)
BATCH_SIZE = 20
PAUSE_BETWEEN_ISINS = (1.0, 2.0)     # segundos
PAUSE_BETWEEN_BATCHES = (2.0, 3.0)   # segundos

CBONDS_CATEGORIES = ["stocks", "bonds", "indexes", "company", "etf"]

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Session (cloudscraper si está disponible)
try:
    import cloudscraper
    session = cloudscraper.create_scraper()
    session.headers.update(DEFAULT_HEADERS)
    print("> Usando cloudscraper para las peticiones")
except Exception:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    print("> Aviso: cloudscraper no disponible — usando requests.Session()")


# ---------------------------------------------------------
# Utilidades IO + HTTP
# ---------------------------------------------------------
def load_isins_from_excel(path: str, sheet_name: Optional[str] = None) -> Optional[pd.DataFrame]:
    if not os.path.exists(path):
        print(f"ERROR: archivo no encontrado: {path}")
        return None
    try:
        df = pd.read_excel(path, sheet_name=sheet_name)
    except Exception as e:
        print(f"ERROR al leer Excel: {e}")
        return None

    df.columns = df.columns.str.strip().str.upper()

    col_isin = None
    for cand in ["ISIN"]:
        if cand in df.columns:
            col_isin = cand
            break

    col_emisora = None
    for cand in ["EMISORA", "TICKER", "EMISOR", "SYMBOL"]:
        if cand in df.columns:
            col_emisora = cand
            break

    if col_isin is None or col_emisora is None:
        print("ERROR: No se encontraron columnas ISIN y EMISORA (o equivalentes) en el Excel")
        return None

    df = df[[col_isin, col_emisora]].copy()
    df.rename(columns={col_isin: "ISIN", col_emisora: "EMISORA"}, inplace=True)
    df["ISIN"] = df["ISIN"].astype(str).str.strip()
    df["EMISORA"] = df["EMISORA"].astype(str).str.strip()
    df.dropna(subset=["ISIN", "EMISORA"], inplace=True)
    df = df[df["ISIN"].str.len() > 5]
    df.reset_index(drop=True, inplace=True)
    return df


def _safe_get(url: str, retries: int = 2, timeout: int = 20) -> Optional[requests.Response]:
    for intento in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=timeout)
            if resp.status_code == 200:
                return resp
        except:
            time.sleep(1 + random.random())

    try:
        resp = requests.get(url, timeout=timeout, verify=False, headers=DEFAULT_HEADERS)
        if resp.status_code == 200:
            return resp
    except Exception as e:
        print(f"    > Fallback requests falló para {url}: {e}")

    return None


def _normalize_ticker(text: Optional[str]) -> str:
    if not text:
        return ""
    return text.strip().upper().split('.')[0]


# ---------------------------------------------------------
# Extracción (solo filas de tabla que contienen ticker)
# ---------------------------------------------------------
def _header_contains_isin(soup: BeautifulSoup, isin: str) -> bool:
    """Valida si el ISIN aparece en el encabezado (h1/h2/title/meta) de la página."""
    if not isin:
        return False
    u_isin = isin.strip().upper()

    parts = []
    # selectores comunes para encabezado/título
    selectors = [
        "h1#cb_stock_ttl", "h1", "h2",
        ".instrument-header", ".stock-header",
        "title", 'meta[property="og:title"]', 'meta[name="title"]'
    ]
    for sel in selectors:
        el = soup.select_one(sel)
        if not el:
            continue
        if el.name == "meta":
            parts.append(el.get("content", ""))
        else:
            parts.append(el.get_text(" ", strip=True))

    header_blob = " ".join(parts).upper()
    if u_isin in header_blob:
        return True

    # fallback: check small region near top of body (first 800 chars)
    body = soup.body.get_text(" ", strip=True) if soup.body else ""
    if u_isin in body[:1000].upper():
        return True

    return False


def _extract_currency_from_row(tr, target_ticker: str) -> Optional[str]:
    """Dada una fila <tr> intenta extraer el ticker y la moneda; si el ticker coincide devuelve moneda."""
    td_ticker = tr.select_one("td.field_tiker, td[class*='tiker']")
    td_currency = tr.select_one("td.field_currency_name, td[class*='currency']")
    if not td_ticker:
        return None

    # obtener ticker raw
    div_tick = td_ticker.find("div")
    if div_tick and div_tick.has_attr("title"):
        raw_t = div_tick.get('title').strip()
    else:
        sp = td_ticker.find("span")
        raw_t = sp.get_text(strip=True) if sp else td_ticker.get_text(" ", strip=True)

    if not raw_t:
        return None

    # comparar normalized
    if _normalize_ticker(raw_t) != _normalize_ticker(target_ticker):
        return None

    # ahora extraer moneda preferente desde td_currency (title > span > text)
    if not td_currency:
        return None

    div_cur = td_currency.find("div")
    if div_cur and div_cur.has_attr("title"):
        raw_c = div_cur.get("title").strip()
    else:
        spc = td_currency.find("span")
        raw_c = spc.get_text(strip=True) if spc else td_currency.get_text(" ", strip=True)

    if not raw_c:
        return None

    m = __import__("re").search(r"([A-Z]{3})", raw_c.upper())
    return m.group(1).upper() if m else raw_c.strip().upper()


def _find_currency_in_exchange_table(soup: BeautifulSoup, target_ticker: str) -> Tuple[Optional[str], Optional[str]]:
    """Apunta a la tabla exchangeTable preferida y busca una fila con el ticker objetivo."""
    selectors = [
        "div.exchangeTable.table_cntrl2 table.table.full",
        "div.exchangeTable table.table.full",
        "div.table_wrapper table.table.full",
        "table.table.full"
    ]
    for sel in selectors:
        table = soup.select_one(sel)
        if not table:
            continue
        rows = table.select("tbody tr") or table.select("tr")
        for tr in rows:
            currency = _extract_currency_from_row(tr, target_ticker)
            if currency:
                return currency, "OK: tabla exchangeTable (ticker encontrado)"
    return None, "Ticker no encontrado en exchangeTable"


def _find_currency_anywhere(soup: BeautifulSoup, target_ticker: str) -> Tuple[Optional[str], Optional[str]]:
    """Búsqueda amplia por filas en cualquier tabla; devuelve moneda solamente si encuentra fila con ticker coincidente."""
    tds = soup.select("td.field_tiker, td[class*='tiker']")
    if not tds:
        tds = soup.find_all("td")
    for td in tds:
        parent_tr = td.find_parent("tr")
        if not parent_tr:
            continue
        currency = _extract_currency_from_row(parent_tr, target_ticker)
        if currency:
            return currency, "OK: fila encontrada en búsqueda amplia"
    return None, "Ticker no encontrado en búsqueda amplia"


# ---------------------------------------------------------
# Orquestador (con verificación ISIN en encabezado)
# ---------------------------------------------------------
def obtener_moneda_cbonds(isin: str, ticker_objetivo: Optional[str]) -> Dict[str, Optional[str]]:
    resultado = {"isin": isin, "ticker": ticker_objetivo, "url": None, "moneda": None, "motivo": None, "categoria": None}
    header_seen_any = False
    # Recorremos categorías; si al final ninguna tenía el ISIN -> ISIN no coincide
    for categoria in CBONDS_CATEGORIES:
        url = f"https://cbonds.com/{categoria}/{isin}/"
        resp = _safe_get(url)
        if not resp:
            continue

        try:
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            soup = BeautifulSoup(resp.text, "html.parser")

        # Verificar que el ISIN esté en el encabezado de la página
        if not _header_contains_isin(soup, isin):
            # no es la página del ISIN (o no aparece en encabezado) -> intentar siguiente categoría
            # no marcamos fallo definitivo todavía
            print(f"  > {categoria}: ISIN no aparece en encabezado de página (continuando).")
            continue

        # si llegamos aquí, el encabezado contiene el ISIN en esta categoría
        header_seen_any = True

        # Intento estricto 1: tabla exchangeTable (preferida)
        moneda, motivo = _find_currency_in_exchange_table(soup, ticker_objetivo)
        if moneda:
            resultado.update({"url": url, "moneda": moneda, "motivo": motivo, "categoria": categoria})
            return resultado

        # Intento estricto 2: búsqueda amplia por filas, solo si encuentra fila con ticker coincidente
        moneda, motivo = _find_currency_anywhere(soup, ticker_objetivo)
        if moneda:
            resultado.update({"url": url, "moneda": moneda, "motivo": motivo, "categoria": categoria})
            return resultado

    # Si jamás vimos el ISIN en encabezados de ninguna categoría -> ISIN no coincide
    if not header_seen_any:
        resultado.update({"moneda": "N/A", "motivo": "ISIN no coincide", "categoria": None})
        return resultado

    # Si vimos el ISIN en alguna categoría pero nunca encontramos el ticker -> Emisora no coincide
    resultado.update({"moneda": "N/A", "motivo": "Emisora no coincide", "categoria": None})
    return resultado


# ---------------------------------------------------------
# Procesamiento por lotes con prints en tiempo real
# ---------------------------------------------------------
def procesar_lotes_cbonds(df_pairs: pd.DataFrame, out_file: str = OUTPUT_FILE) -> pd.DataFrame:
    results = []
    total = len(df_pairs)
    if total == 0:
        print("No hay pares ISIN/Emisora para procesar.")
        return pd.DataFrame()

    num_batches = math.ceil(total / BATCH_SIZE)
    processed = 0

    try:
        for batch_idx in range(num_batches):
            start = batch_idx * BATCH_SIZE
            end = min(start + BATCH_SIZE, total)
            batch = df_pairs.iloc[start:end]
            print(f"\nProcesando lote {batch_idx + 1}/{num_batches}: registros {start + 1} a {end} ({len(batch)})")

            for _, row in batch.iterrows():
                processed += 1
                isin = str(row['ISIN']).strip()
                emisora = str(row['EMISORA']).strip()

                res = obtener_moneda_cbonds(isin, emisora)
                results.append(res)

                moneda_to_show = res.get("moneda") if res.get("moneda") else "N/A"
                motivo_to_show = res.get("motivo") or ""
                categoria_to_show = res.get("categoria") or "-"
                print(f"[{processed}/{total}] {isin} ({emisora}) -> moneda: {moneda_to_show} | motivo: {motivo_to_show} | categoría: {categoria_to_show}")

                # pausa aleatoria entre ISINs
                time.sleep(random.uniform(*PAUSE_BETWEEN_ISINS))

            # Guardar resultados parciales tras cada lote (resiliencia)
            df_partial = pd.DataFrame(results)
            try:
                df_partial.to_excel(out_file, index=False)
                print(f"  > Resultados parciales guardados en: {out_file} (lote {batch_idx+1})")
            except Exception as e:
                print(f"  > ERROR al guardar resultados parciales: {e}")

            # Pausa entre lotes si no es el último
            if batch_idx < num_batches - 1:
                pause = random.uniform(*PAUSE_BETWEEN_BATCHES)
                print(f"  > Pausa entre lotes: {pause:.1f} seg")
                time.sleep(pause)

    except KeyboardInterrupt:
        print("\nInterrupción por usuario: guardando progreso parcial...")
        df_partial = pd.DataFrame(results)
        try:
            df_partial.to_excel(out_file, index=False)
            print(f"Progreso guardado en: {out_file}")
        except Exception as e:
            print(f"ERROR al guardar progreso: {e}")
        sys.exit(1)

    df_results = pd.DataFrame(results)
    try:
        df_results.to_excel(out_file, index=False)
        print(f"\nResultados finales guardados en: {out_file}")
    except Exception as e:
        print(f"ERROR al guardar resultados finales: {e}")

    return df_results


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == '__main__':
    print("Inicio cbonds_batch_strict.py")
    df_pairs = load_isins_from_excel(INPUT_FILE, INPUT_SHEET)
    if df_pairs is None or df_pairs.empty:
        print("No hay datos para procesar. Verifica el archivo de entrada y las columnas.")
        sys.exit(0)

    print(f"Se han cargado {len(df_pairs)} pares ISIN/Emisora para procesar.")
    df_out = procesar_lotes_cbonds(df_pairs, out_file=OUTPUT_FILE)

    # Resumen
    if df_out is not None and not df_out.empty:
        total = len(df_out)
        ok = (df_out['moneda'].notna()) & (df_out['moneda'] != '') & (df_out['moneda'] != 'N/A')
        n_ok = ok.sum()
        print('\n--- RESUMEN ---')
        print(f'Total procesados: {total}')
        print(f'Encontradas monedas: {n_ok} ({n_ok/total:.1%})')
        print('Columnas de salida: ', ', '.join(df_out.columns.tolist()))
    else:
        print('No se obtuvieron resultados.')

    print('Fin.')
