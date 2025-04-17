import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    for td in soup.find_all('td', class_='ads_price'):
        price = td.get_text(strip=True)
        if '€' in price:
            return price

    return "Price not found"


url = 'https://www.ss.com/msg/lv/electronics/computers/game-consoles/kbdmi.html'
print("PS5 Price on ss.com:", get_price(url))






