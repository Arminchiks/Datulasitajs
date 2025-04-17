import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_amazon_price(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle")
    price = soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_dealprice")
    return {
        "site": "Amazon",
        "title": title.get_text(strip=True) if title else "N/A",
        "price": price.get_text(strip=True) if price else "N/A",
        "url": url
    }

def get_ebay_price(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h1", {"class": "x-item-title__mainTitle"})
    price = soup.find("span", {"itemprop": "price"})
    return {
        "site": "eBay",
        "title": title.get_text(strip=True) if title else "N/A",
        "price": price.get_text(strip=True) if price else "N/A",
        "url": url
    }

def get_sscom_price(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find("h2", {"class": "page-header"})
    price = soup.find("span", {"class": "price"})
    return {
        "site": "SS.com",
        "title": title.get_text(strip=True) if title else "N/A",
        "price": price.get_text(strip=True) if price else "N/A",
        "url": url
    }

def compare_prices(product_urls):
    results = []
    for site, url in product_urls.items():
        if site == "Amazon":
            results.append(get_amazon_price(url))
        elif site == "eBay":
            results.append(get_ebay_price(url))
        elif site == "SS.com":
            results.append(get_sscom_price(url))
    return results

# Example usage:
product_urls = {
    "Amazon": "https://www.amazon.com/dp/B09G3HRMVB/",
    "eBay": "https://www.ebay.com/itm/234567890123",
    "SS.com": "https://www.ss.com/msg/en/electronics/computers/computers/desktop-computers/abcd1234.html"
}

results = compare_prices(product_urls)

# Print results in a table
print(f"{'Site':<10} {'Title':<40} {'Price':<15} {'URL'}")
for r in results:
    print(f"{r['site']:<10} {r['title'][:37]:<40} {r['price']:<15} {r['url']}")
