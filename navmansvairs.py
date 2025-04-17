from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox

def get_price_selenium(url):
    options = Options()
    options.add_argument("--headless")  # No GUI
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.quit()

    for td in soup.find_all("td", class_="ads_price"):
        price = td.get_text(strip=True)
        if "€" in price:
            return price

    return "Price not found"

def fetch_price():
    url = url_entry.get()
    if not url.startswith("http"):
        messagebox.showwarning("Invalid URL", "Please enter a valid URL (must start with http or https).")
        return

    price = get_price_selenium(url)
    result_label.config(text=f"Price: {price}")

# --- Tkinter UI ---
root = tk.Tk()
root.title("PS5 Price Checker (with Selenium)")
root.geometry("400x200")

tk.Label(root, text="Enter ss.com URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
tk.Button(root, text="Check Price", command=fetch_price).pack(pady=10)
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=5)

root.mainloop()
