import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, *args, **kwargs):
        self.link = ''
        self.price = 0
        self.title = ''


def get_page_for_amazon_book_search(keyword):
    search_string = (
        'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias'
        '%3Dstripbooks&field-keywords={search_string}'
        '&rh=n%3A283155%2Ck%3A{search_string}'.format(
            search_string=keyword,
        )
    )
    return requests.get(search_string).content


def get_amazon_book_prices_for_keyword(keyword):
    content = get_page_for_amazon_book_search(keyword)
    soup = BeautifulSoup(content)
    list_items = soup.find_all('li', class_='s-result-item celwidget')
    for item in list_items:
        print item.find_all(
            'span',
            class_='a-size-base a-color-price s-price a-text-bold',
        )


def get_page_for_google_books_book_search(keyword):
    search_string = (
        'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias'
        '%3Dstripbooks&field-keywords={search_string}'
        '&rh=n%3A283155%2Ck%3A{search_string}'.format(
            search_string=keyword,
        )
    )
    return requests.get(search_string).content


def get_google_books_book_prices_for_keyword(keyword):
    content = get_page_for_google_books_book_search(keyword)
    soup = BeautifulSoup(content)
    list_items = soup.find_all('li', class_='s-result-item celwidget')
    for item in list_items:
        print item.find_all(
            'span',
            class_='a-size-base a-color-price s-price a-text-bold',
        )


get_google_books_book_prices_for_keyword('compilers')
