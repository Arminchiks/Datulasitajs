import requests
from bs4 import BeautifulSoup
import smtplib

def get_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find('span', {'ads_opt': 'ads_price'})['content']
    return price


cpu = get_price('https://www.ss.com/msg/lv/electronics/computers/game-consoles/blepfk.html')

total_price = (cpu)
print(total_price)