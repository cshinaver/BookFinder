import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, *args, **kwargs):
        self.link = ''
        self.price = 0
        self.title = ''
        self.book_type = ''
        self.is_rental = False

    def __str__(self):
        return (
            "Title: {title}\n"
            "Price: {price}\n"
            "rental: {rental}\n"
            "book type: {book_type}\n"
            "link: {link}\n".format(
                title=self.title,
                price=self.price,
                rental=self.is_rental,
                book_type=self.book_type,
                link=self.link,
            )
        )


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

get_amazon_book_prices_for_keyword('compilers')
