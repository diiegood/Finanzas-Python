import re
from typing import Optional, Dict

import requests
from bs4 import BeautifulSoup
import urllib3

# --- Configuración -----------------------------------------------------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# Session (cloudscraper si está disponible)
try:
    import cloudscraper  # type: ignore
    session = cloudscraper.create_scraper()
    session.headers.update(DEFAULT_HEADERS)
    print("> Usando cloudscraper: session creada con cabeceras por defecto")
except Exception:
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)
    print("> Aviso: cloudscraper no disponible. Usando requests.Session() con cabeceras por defecto")


def _safe_get(url: str, timeout: int = 20, allow_insecure_fallback: bool = True, **kwargs) -> requests.Response:
    """GET con manejo de SSL; no escribe nada a disco."""
    try:
        r = session.get(url, timeout=timeout, **kwargs)
        r.raise_for_status()
        return r
    except requests.exceptions.SSLError:
        if allow_insecure_fallback:
            r = session.get(url, timeout=timeout, verify=False, **kwargs)
            r.raise_for_status()
            return r
        raise


def _normalize_ticker(text: Optional[str]) -> str:
    if not text:
        return ""
    t = text.strip().upper()
    # Normalizamos eliminando sufijos tras el punto (ej. TRN.P -> TRN)
    return t.split('.')[0]


def _extract_currency_from_rows_anywhere(soup: BeautifulSoup, ticker: Optional[str]) -> Optional[str]:
    """Busca filas que contengan el ticker en cualquier tabla/parte del HTML y extrae la moneda

    Estrategia robusta:
    - Buscar todos los <td> que tengan la clase 'field_tiker' (o variantes con 'tiker' en el nombre de clase).
    - Para cada TD candidato: extraer el ticker (preferir title del <div>, luego <span>, luego texto).
    - Si coincide con el ticker pedido (normalizado), tomar el <tr> padre y extraer el <td> con clase que contenga 'currency'.
    - Extraer preferentemente title del <div> dentro del td de moneda, luego <span>, luego texto.
    - Validar que la moneda parezca un código (3 letras mayúsculas) antes de devolver.
    """
    if not ticker:
        return None
    target = _normalize_ticker(ticker)

    # Buscador amplio para tds que contienen el ticker (clase exacta o que contenga la palabra 'tiker')
    tds = soup.select('td.field_tiker') or soup.select('td[class*="tiker"]')
    if not tds:
        # Intento más amplio por si la página usa otra rotulación de clases
        tds = soup.find_all('td')

    for td in tds:
        # extraer texto del ticker (title de div > span > texto)
        raw_ticker = None
        div = td.find('div')
        if div and div.get('title'):
            raw_ticker = div.get('title').strip()
        else:
            sp = td.find('span')
            if sp:
                raw_ticker = sp.get_text(strip=True)
            else:
                raw_ticker = td.get_text(' ', strip=True)

        if not raw_ticker:
            continue

        norm = _normalize_ticker(raw_ticker)

        # Coincidencia flexible: prioridad exacta sobre prefix (TRN.P) sobre containment
        matched = False
        if norm == target:
            matched = True
        else:
            ru = raw_ticker.upper()
            if ru.startswith(target + '.'):
                matched = True
            elif target in ru:
                matched = True

        if not matched:
            continue

        # Encontramos el tr padre
        tr = td.find_parent('tr')
        if not tr:
            continue

        # Intentamos extraer el td de moneda dentro de la misma fila
        td_curr = tr.select_one('td.field_currency_name, td.field_currency, td[class*="field_currency"], td[class*="currency"]')

        # Si no hay td con clase explícita, hacemos heurística por posición relativa (buscamos la celda que visualmente parece 'Currency')
        if not td_curr:
            tds_in_row = tr.find_all('td')
            # buscamos una celda cuyo texto contenga 'Currency' o 'Moneda' o que tenga 'currency' en su clase
            for c in tds_in_row:
                ccls = ' '.join(c.get('class') or [])
                txt = c.get_text(' ', strip=True).lower()
                if 'currency' in ccls or 'currency' in txt or 'moneda' in txt or 'divisa' in txt:
                    td_curr = c
                    break

        if not td_curr:
            # No se encontró la celda de moneda en esta fila concreta
            continue

        # Extraer texto de moneda preferente (title de div > span > texto)
        divc = td_curr.find('div')
        curr_raw = None
        if divc and divc.get('title'):
            curr_raw = divc.get('title').strip()
        else:
            spc = td_curr.find('span')
            if spc:
                curr_raw = spc.get_text(strip=True)
            else:
                curr_raw = td_curr.get_text(' ', strip=True)

        if not curr_raw:
            continue

        # Validamos que sea algo parecido a 'USD' o 'EUR' (tres letras) — aquí buscamos la primera aparición de 3 letras mayúsculas
        m = re.search('([A-Z]{3})', curr_raw.upper())
        if m:
            return m.group(1).upper()
        # Si no hay bloque de 3 letras, devolvemos el string limpio (por si la página usa formatos raros)
        cr = curr_raw.strip().upper()
        if 2 < len(cr) <= 5:
            return cr

    return None


def _extract_currency_from_embedded_json(soup: BeautifulSoup) -> Optional[str]:
    """Fallback: busca claves de moneda en scripts embebidos (bastante conservador)."""
    keys = ['currency', 'currencyCode', 'tradingCurrency', 'quote_currency', 'currency_code']
    scripts = soup.find_all('script')
    for s in scripts:
        txt = s.string or s.get_text() or ''
        lower = txt.lower()
        for k in keys:
            if k.lower() in lower:
                # tomar una ventana alrededor de la primera aparición
                idx = lower.find(k.lower())
                window = txt[idx: idx + 200]
                m = re.search('([A-Z]{3})', window)
                if m:
                    return m.group(1).upper()
    return None


def obtener_datos_cbonds(isin: str, ticker_objetivo: Optional[str] = None) -> Dict[str, Optional[str]]:
    categorias = ['stocks', 'bonds', 'indexes', 'company', 'etf']

    resultado = {'isin': isin, 'ticker': ticker_objetivo, 'url': None, 'moneda': None, 'motivo': None}

    for categoria in categorias:
        url = f'https://cbonds.com/{categoria}/{isin}/'
        try:
            resp = _safe_get(url)
            print(f'  > Intentando categoría: {categoria} -> {url} | Status: {resp.status_code}')
        except requests.RequestException as exc:
            print(f'    > Error al conectar a {url}: {exc} (se intenta siguiente categoría)')
            continue

        soup = BeautifulSoup(resp.text, 'lxml')

        # Validación básica del encabezado: que al menos el ISIN aparezca en el <h1> o cerca
        h1 = soup.select_one('h1')
        encabezado_text = h1.get_text(' ', strip=True) if h1 else ''
        if isin.upper() not in encabezado_text.upper():
            print('    > Encabezado no contiene ISIN; se intenta la siguiente categoría.')
            continue

        # 1) Buscar la moneda en filas de la tabla (no dependemos de una tabla específica)
        moneda = _extract_currency_from_rows_anywhere(soup, ticker_objetivo) if ticker_objetivo else None
        if moneda:
            resultado.update({'url': url, 'moneda': moneda, 'motivo': 'OK: tabla (fila con ticker)'})
            return resultado

        # 2) Intentar JSON embebido (fallback controlado)
        moneda = _extract_currency_from_embedded_json(soup)
        if moneda:
            resultado.update({'url': url, 'moneda': moneda, 'motivo': 'OK: json embebido'})
            return resultado

        # 3) Heurística muy limitada en body (último recurso)
        body_text = soup.body.get_text(' ', strip=True) if soup.body else ''
        m = re.search('([A-Z]{3})', body_text)
        if m:
            found = m.group(1).upper()
            resultado.update({'url': url, 'moneda': found, 'motivo': 'OK: heurística restringida (body)'})
            return resultado

    resultado['motivo'] = 'No se encontró moneda (búsqueda finalizada sin éxito)'
    return resultado


# --- Test rápido con tu fila (puedes ejecutar este script localmente) --------
if __name__ == '__main__':
    # Caso real que compartiste
    row_html = '''<tr id="exchangeTable_scroll_item_0" data-index="0" class="greenback odd"><td id="cb_exchangeTable_scroll_item_first_0"><div class="table-with-checkbox"><div><span>NYSE</span> <span class="mainTradingGround">Main Exchange</span></div></div></td><td id="cb_exchangeTable_scroll_item_0_1" class="field_date"><div title="02/09/2025 17:43"><div><span>02/09/2025 17:43</span></div></div></td><td id="cb_exchangeTable_scroll_item_0_2" class="field_last"><div title=""><span class="asterisks"><a href="https://cbonds.com/registration/">***</a></span></div></td><td id="cb_exchangeTable_scroll_item_0_8" class="field_tiker"><div title="TRN"><div><span>TRN</span></div></div></td><td id="cb_exchangeTable_scroll_item_0_9" class="field_currency_name"><div title="USD"><div><span>USD</span></div></div></td></tr>'''

    # Construimos un doc HTML mínimo que contenga la fila dentro de una tabla
    html_doc = f"<html><body><table class=\"table full\"><tbody>{row_html}</tbody></table></body></html>"
    soup = BeautifulSoup(html_doc, 'lxml')

    moneda = _extract_currency_from_rows_anywhere(soup, 'TRN')
    print('Prueba con fila de ejemplo -> moneda encontrada:', moneda)

    # Test real via web
    isin_test = 'GB00B1N7Z094'
    ticker_test = 'SAFE'
    print('--- PRUEBA DE SCRAPING CBONDS (sin guardar HTML) ---')
    res = obtener_datos_cbonds(isin_test, ticker_test)
    for k, v in res.items():
        print(f"{k}: {v}")
    print('-------------------')
