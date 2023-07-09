import json
import re
import requests
from bs4 import BeautifulSoup
from helper import *


def scrap(url: str) -> float:
    with requests.Session() as session:
        session.headers = {
            "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/70.0.3538.110 Safari/537.36''',
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
    try:
        response = session.get(url)
    except requests.exceptions.MissingSchema:
        return float('inf')
    soup = BeautifulSoup(response.text, 'html.parser')

    s = re.search(r'[-\w]+(?=\.\w{2,3}/)', url)
    cl = shops[s.group()]

    try:
        price = soup.select_one(cl).text.strip()

        if "zł" in price:
            to = price.find(' zł')
        else:
            to = None

        p = float(price.replace(',', '.')[:to].replace('\xa0', '').replace(' ', ''))
    except:
        # print(f"Problem while parsing {url} and its price is")
        # print(price)
        return float('inf')

    return p

def get_parts_prices(parts_json: dict) -> dict:
    parts = dict()
    i = 0
    for key in parts_json:
        i += 1
        printScraping(i, len(parts_json))

        parts[key] = [parts_json[key][0], None, None]

        prices = []
        for in_key, url in parts_json[key][1].items():
            prices.append((in_key, scrap(url)))

        price = min(prices, key=lambda _: _[1])

        parts[key][1] = price[0]
        parts[key][2] = price[1]
    return parts

def print_result(parts: dict) -> None:
    total = 0

    print("\r", end='')
    for key, value in parts.items():
        printValue(key, value)
        total += value[2]

    print(f"\nBest price of whole setup is {total:.2f} zł.")

def main(json_file: str):
    with open(json_file) as f:
        parts_json = json.load(f)

    parts = get_parts_prices(parts_json)
    print_result(parts)
    saveFile(parts)


if __name__ == '__main__':
    main('parts.json')


# proline:
# 	ENDORFY Signum 300 ARGB - 354.99 zł
# 	ENDORFY Fera 5 ARGB - 163.00 zł
# 	Thermal Grizzly Kryonaut 1g - 33.80 zł
# 	----Total in proline: 551.79 zł
