import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

SEARCH_URLS = {
    'ss.com': 'https://www.ss.com/lv/electronics/computers/game-consoles/filter/',
    'kurpirkt.lv': 'https://www.kurpirkt.lv/cena.php?q=ps5',
    'amazon.de': 'https://www.amazon.de/s?k=ps5'
}

MIN_PRICE = 100

def parse_price(text):
    match = re.search(r'(\d+[\.,]?\d+)', text.replace('\xa0', '').replace(',', '.'))
    return float(match.group(1)) if match else None

def fetch_ss_com():
    try:
        r = requests.get(SEARCH_URLS['ss.com'], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        listings = soup.select("tr[id^='tr_']")
        results = []

        for listing in listings:
            title_tag = listing.select_one('a[href^="/msg"]')
            price_tag = listing.select_one('td:nth-child(6)')
            if not title_tag or not price_tag:
                continue

            title = title_tag.text.strip().lower()
            if 'ps5' not in title or 'ps4' in title:
                continue

            price = parse_price(price_tag.text)
            if price and price >= MIN_PRICE:
                url = "https://www.ss.com" + title_tag['amopt']
                results.append((price, url, title))

        return min(results, key=lambda x: x[0]) if results else None
    except Exception as e:
        print(f"ss.com error: {e}")
        return None

def fetch_kurpirkt():
    try:
        r = requests.get(SEARCH_URLS['kurpirkt.lv'], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.select('div.result-item')
        results = []

        for item in items:
            link_tag = item.select_one('a[href]')
            price_tag = item.select_one('.price')
            if not link_tag or not price_tag:
                continue

            title = link_tag.text.strip().lower()
            if 'ps5' not in title or 'ps4' in title:
                continue

            price = parse_price(price_tag.text)
            if price and price >= MIN_PRICE:
                url = "https://www.kurpirkt.lv" + link_tag['href']
                results.append((price, url, title))

        return min(results, key=lambda x: x[0]) if results else None
    except Exception as e:
        print(f"kurpirkt.lv error: {e}")
        return None

def fetch_amazon():
    try:
        r = requests.get(SEARCH_URLS['amazon.de'], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []

        for item in soup.select('div.s-result-item'):
            title_tag = item.select_one('h2 a')
            price_tag = item.select_one('.a-price .a-offscreen')
            if not title_tag or not price_tag:
                continue

            title = title_tag.text.strip().lower()
            if 'ps5' not in title or 'ps4' in title:
                continue

            price = parse_price(price_tag.text)
            if price and price >= MIN_PRICE:
                url = "https://www.amazon.de" + title_tag['href'].split("?")[0]
                results.append((price, url, title))

        return min(results, key=lambda x: x[0]) if results else None
    except Exception as e:
        print(f"amazon.de error: {e}")
        return None

def compare_prices():
    sites = {
        "ss.com": fetch_ss_com(),
        "kurpirkt.lv": fetch_kurpirkt(),
        "amazon.de": fetch_amazon()
    }

    print("PS5 Price Comparison (prices in EUR, minimum €100):\n")
    for site, data in sites.items():
        if data:
            price, link, title = data
            print(f"{site}: €{price:.2f} - {title}\n{link}\n")
        else:
            print(f"{site}: No valid PS5 listings found.\n")

    valid = {k: v for k, v in sites.items() if v}
    if valid:
        best_site = min(valid.items(), key=lambda x: x[1][0])
        print(f"Best deal: {best_site[0]} at €{best_site[1][0]:.2f}")
        print(f"Link: {best_site[1][1]}")
    else:
        print("No PS5 listings found on any site.")

if __name__ == "__main__":
    compare_prices()
