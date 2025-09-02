import requests
from bs4 import BeautifulSoup
import urllib3

# Silenciar warnings si usamos verify=False
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


def get_url(isin):
    """Busca el ISIN en MarketScreener y devuelve la URL del primer resultado."""
    search_url = "https://www.marketscreener.com/search/"
    params = {"q": isin}

    try:
        r = requests.get(search_url, params=params, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.exceptions.SSLError:
        r = requests.get(search_url, params=params, headers=HEADERS, timeout=20, verify=False)
        r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    first_result = soup.select_one("table tbody tr td span a")
    if not first_result:
        return None
    return "https://www.marketscreener.com" + first_result["href"]


def get_currency_from_url(url):
    """Extrae la divisa de la página de la acción dada su URL."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.exceptions.SSLError:
        r = requests.get(url, headers=HEADERS, timeout=20, verify=False)
        r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Selector exacto para la divisa
    currency_elem = soup.select_one("td.is__realtime-last sup span")
    if currency_elem:
        return currency_elem.text.strip()
    return "N/A"  # si no encuentra, devuelve N/A


def currency_from_isin(isin):
    """Función principal: busca un ISIN y devuelve la divisa."""
    url = get_url(isin)
    if not url:
        return "N/A", None

    currency = get_currency_from_url(url)
    return currency, url


# -------------------------
# Ejemplo de uso
# -------------------------
isin_test = "US9311421039"
currency, found_url = currency_from_isin(isin_test)

print("ISIN:", isin_test)
print("URL encontrada:", found_url)
print("Moneda:", currency)