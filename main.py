"""
Password Generator

Description:
- Allow user to specify length
- Scrape web for phrase that matches specified length
- Apply "encryption" algorithm to selected word combination
"""


import random
from urllib.request import urlopen
import re
import logging


# Configure logging
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def scrap_url(url):
    """Scrap a url and return html text"""
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html


def word_by_word(text, password_len):
    word = ""
    chosen_text = ""
    pattern = r"([A-Z])"

    for char in text.lower():
        if char.isalpha():
            word += char
        else:
            chosen_text += word.title()
            word = ""

        chosen_text = chosen_text.replace("For", "4")
        chosen_text = chosen_text.replace("At", "@")
        chosen_text = chosen_text.replace("And", "&")
        chosen_text = chosen_text.replace("You", "U")

        if len(chosen_text) == password_len:
            break
        elif len(chosen_text) > password_len:
            result = re.findall(pattern, chosen_text)
            index = chosen_text.find(result[1])
            chosen_text = chosen_text[index:]

    return chosen_text


# TODO: If website returns status code 404, try another random number,
#   "urllib.error.HTTPError: HTTP Error 404: Not Found"
def find_phrase(password_len: int):
    """Find phrase of specified length in random book"""
    # Randomly pick a book
    book_num = random.randrange(1, 1000)
    book_url = f"http://gutenberg.org/files/{book_num}/"
    logging.info(book_url)

    # Search book url for book text url
    pattern = r"href=\"(.+\.txt)\""
    result = re.search(pattern, scrap_url(book_url))
    book_txt_url = f"http://gutenberg.org/files/{book_num}/{result[1]}"
    logging.info(book_txt_url)

    # Extract book text
    book_text = scrap_url(book_txt_url)

    # Search book text word by word
    return word_by_word(book_text, password_len)


def encrypt_text(text):
    """Apply "encryption" algorithm to selected word combination"""
    text = text.replace("O", "0")
    text = text.replace("e", "3")
    text = text.replace("s", "5")
    text = text.replace("i", "!")
    text = text.replace("S", "$")
    return text


if __name__ == '__main__':
    # Collect password length from user
    password_len = input("Specify password length: ")
    while not password_len.isnumeric():
        password_len = input("Specify password length: ")

    # Scrape web for phrase that matches specified length, minus empty space
    phrase = find_phrase(int(password_len))

    # Encrypt chosen phrase
    password = encrypt_text(phrase)
    print(password)
