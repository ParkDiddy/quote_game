import requests
from bs4 import BeautifulSoup
import re
from random import choice


def get_quote_data(max_iterations=100):
    counter = 0
    page_num = 1
    quotes_list = []  # will be a list of dictionaries with keys of quote, author and author link

    while True:
        if counter == max_iterations:
            return choice(quotes_list)
        counter += 1
        url = f"https://quotes.toscrape.com/page/{page_num}/"
        response = requests.get(url)
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


def add_author_clues():
    random_quote = get_quote_data()
    author_page = requests.get(f"https://quotes.toscrape.com{random_quote.get('author_link')}")
    soup = BeautifulSoup(author_page.text, "html.parser")
    clues = soup("div", class_="author-details")

    for clue in clues:
        birthdate = clue.find("span", class_="author-born-date").get_text()
        birthplace = clue.find("span", class_="author-born-location").get_text()
        random_quote.update({"birthdate": birthdate, "birthplace": birthplace})
    return random_quote


def play_game():
    quote = add_author_clues()  # instantiates author clues function which instantiates random quote
    guesses_left = 4
    current_hint = 0
    author = quote.get('author')
    clues_list = [f"Nope! Here's a hint: They were born on {quote.get('birthdate')} "
                  f"{quote.get('birthplace')}",

                  f"Nope! Here's a hint: Their first letter of their first name is {author[0]}",

                  f"Nope! Here's a hint: Their first letter of their last name is {author.split()[1][0]}"]

    print("Welcome to the quote game! I will give you a quote and you need to guess who said it!")
    print(quote.get("quote"))

    while guesses_left != 0:
        print(f"You have {guesses_left} guesses left.")
        guess = input("Enter your guess here:\n")
        if guess.title() != author and guesses_left > 0:
            guesses_left -= 1
            if guesses_left == 0:
                print(f"Sorry, you lost! The author was {author}.")
                break
            print(clues_list[current_hint])
            current_hint += 1
            continue
        if guess.title() == author:
            print("You got it!!! Nice job.")
        break

    play_again = input("Would you like to play again? (y/n)\n")
    if play_again == "y":
        play_game()
    print("Thanks for playing!")
    return


if __name__ == "__main__":
    play_game()
