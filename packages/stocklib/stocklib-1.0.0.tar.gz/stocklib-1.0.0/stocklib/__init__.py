import requests
from bs4 import BeautifulSoup


def get_stock_price(ticker: str):
    ticker = ticker.capitalize()
    url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    return float(soup.find_all("div", class_="YMlKec fxKbKc")[0].string.replace("$", ""))
