import requests
from bs4 import BeautifulSoup
import re
from random import choice


def get_quote_data():
    page_num = 1

    quotes_list = []  # will be a list of dictionaries with keys of quote, author and author link

    while True:
        response = requests.get(f"https://quotes.toscrape.com/page/{page_num}/")
        soup = BeautifulSoup(response.text, "html.parser")
        text = str(soup("div", class_="col-md-8"))

        if not re.search(r'No quotes found!', text):
            quotes = soup("div", class_="quote")
            for quote in quotes:
                quote_text = quote.find("span", class_="text").get_text()
                author = quote.find("small", class_="author").get_text()
                author_link = quote.find("a")["href"]
                quotes_list.append(dict(quote=quote_text, author=author, author_link=author_link))
            page_num += 1

        else:
            return choice(quotes_list)


random_quote = get_quote_data()

print(random_quote.get("quote") + " by " + random_quote.get("author"))