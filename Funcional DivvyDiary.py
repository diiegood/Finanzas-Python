import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
}

def get_currency_divvy_single(isin):
    base_url = f"https://divvydiary.com/en/{isin}"
    
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=20, verify=False)
        r.raise_for_status()
        final_url = r.url
    except requests.exceptions.RequestException:
        return "N/A", base_url
    
    soup = BeautifulSoup(r.text, "html.parser")

    # Buscar específicamente "Dividend Currency"
    for dt in soup.find_all("dt"):
        if dt.get_text(strip=True).lower() == "dividend currency":
            dd = dt.find_next_sibling("dd")
            if dd:
                return dd.get_text(strip=True), final_url

    return "N/A", final_url


# -------------------------------
# Probar 1 ISIN
# -------------------------------
isin_test = "FR0000120628"
currency, final_url = get_currency_divvy_single(isin_test)
print(f"ISIN: {isin_test}")
print(f"URL final: {final_url}")
print(f"Currency DivvyDiary: {currency}")