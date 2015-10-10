import requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

class PurchaseOption:
    def __init__(self, *args, **kwargs):
        self.link = ''
        self.price = 0
        self.seller = ''
        self.book_type = ''
        self.is_rental = False
        self.purchaseID = ''

    def __str__(self):
        return (
            "Seller: {seller}\n"
            "Price: {price}\n"
            "rental: {rental}\n"
            "book type: {book_type}\n"
            "link: {link}\n"
            "PurchaseID: {purchaseID}\n".format(
                seller=self.seller,
                price=self.price,
                rental=self.is_rental,
                book_type=self.book_type,
                link=self.link,
                purchaseID=self.purchaseID,
            )
        )

    def __repr__(self):
        return (
            "Seller: {seller}\n"
            "Price: {price}\n"
            "rental: {rental}\n"
            "book type: {book_type}\n"
            "link: {link}\n"
            "PurchaseID: {purchaseID}\n".format(
                seller=self.seller,
                price=self.price,
                rental=self.is_rental,
                book_type=self.book_type,
                link=self.link,
                purchaseID=self.purchaseID,
            )
        )

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

    def __repr__(self):
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


def get_amazon_books_for_keyword(keyword):
    def get_book_list_items_from_content(content):
        """ Returns Amazon book items in BeautifulSoup format """
        soup = BeautifulSoup(content, 'html.parser')
        book_list_items = soup.find_all('li', class_='s-result-item celwidget')
        return book_list_items

    def parse_price_bulk_item_into_book(item, title):
        new_book = Book()
        price_tag = item.find(
            'span',
            class_="a-size-base a-color-price s-price a-text-bold",
        )

        # if does not contain price, ignore
        if not price_tag:
            return

        new_book.price = price_tag.get_text()
        link = item.attrs['href']
        # Amazon links have weird &amp; in them which breaks them
        # Remove anything after the first & arg
        new_book.link = link[:link.find('&')]
        new_book.title = title

        # determine if is rental
        rent_or_buy_item = item.find(
            'span',
            class_='a-color-secondary',
        )
        if rent_or_buy_item:
            rent_or_buy_text = rent_or_buy_item.get_text()
            new_book.is_rental = "rent" in rent_or_buy_text

        return new_book

    def parse_book_list_item_into_books(item):
        def get_book_type(item):
            text = item.get_text()
            if "$" in text:
                return ''
            else:
                return text

        # Title and link contained in link element
        link_item = item.find(
            'a',
            class_="a-link-normal s-access-detail-page a-text-normal",
        )
        new_book_title = link_item.attrs['title']

        # Handle pricing for hardcover, Paperback, Kindle Edition, rent
        price_column_item = item.find('div', class_="a-column a-span7")
        price_bulk_items = price_column_item.find_all(
            'a',
            class_='a-link-normal a-text-normal',
        )

        new_books = []
        book_type = ''
        for item in price_bulk_items:
            # First check for book type (Hardcover, softcover, etc)
            new_book_type = get_book_type(item)
            if new_book_type:
                book_type = new_book_type
                continue
            book = parse_price_bulk_item_into_book(item, new_book_title)
            book.book_type = book_type
            if book:
                new_books.append(book)
        return new_books

    content = get_page_for_amazon_book_search(keyword)
    items = get_book_list_items_from_content(content)
    book_lists = map(parse_book_list_item_into_books, items)
    return [item for sublist in book_lists for item in sublist]




def money_to_dec(money_str):
    return Decimal(sub(r'[^\d.]', '', money_str))


def get_google_books_search_page_for_isbn(isbn):
    search_string = (
        'https://books.google.com/books?isbn='
        '{search_string}'.format(search_string=isbn,)
    )
    return requests.get(search_string).content


def extract_google_books_page_link_from_li(item):
    h3_item = item.find(
        'h3',
        class_='r',
    )
    a_item = h3_item.find('a')
    return a_item.attrs['href']


def get_google_books_page_link_for_isbn(isbn):
    content = get_google_books_search_page_for_isbn(isbn)
    soup = BeautifulSoup(content)
    item = soup.find('li', class_='g')
    link = extract_google_books_page_link_from_li(item)
    return link


# Sometimes link is a redirect link in google's format.
# This function translates that to a direct link.
def convert_google_redirect_to_direct_link(redir_link):
    link_pos = redir_link.find('&q=') + 3
    if not redir_link.startswith('/url?'):
        return redir_link
    # returns -1 if not found
    if link_pos==2:
        return redir_link
    link_sub = redir_link[link_pos:]
    full_redir_link = 'https://www.google.com/url?rct=j&url=' + link_sub
    content = requests.get(full_redir_link).content
    soup = BeautifulSoup(content)
    body = soup.find('body')
    # if has no body, is probably actually a redirect page - grab the redirect link
    # otherwise, is probably a redirect warning - pull the continue link
    if body==None:
        META = soup.find('meta')
        meta_content = META.attrs['content']
        link = meta_content[7:]
        link = link[:(len(link) - 1)]
    else:
        all_links = soup.find_all('a')
        first_link = all_links[0]
        link = first_link.attrs['href']
    return link


def extract_google_books_price_list_from_link(link):
    content = requests.get(link).content
    soup = BeautifulSoup(content)
    center = soup.find('div', id='volume-center')
    list_area = center.find('div', class_='about_content')
    list_items = list_area.find_all('tr')
    array = []
    for item in list_items:
        price_span = item.find('span', class_='price')
        if price_span!=None:
            seller_link_href = item.find('a')
            seller_name = seller_link_href.text
            seller_link_redir = seller_link_href.attrs['href'] 
            seller_link = convert_google_redirect_to_direct_link(seller_link_redir)
            price_text = price_span.text
            price = money_to_dec(price_text)
            option = PurchaseOption()
            option.link = seller_link
            option.price = price
            option.seller = seller_name
            option.book_type = 'print'
            option.is_rental = False
            option.purchaseID = ''
            array.append(option)
    return array


# Sometimes link is a redirect link in google's format.
# This function translates that to a direct link before extracting.
def extract_google_books_price_list_from_redirect_link(redir_link):
    link = convert_google_redirect_to_direct_link(redir_link)
    return extract_google_books_price_list_from_link(link)


def extract_google_books_prices_from_page_link(link):
    content = requests.get(link).content
    soup = BeautifulSoup(content)
    get_button = soup.find('a', id='gb-get-book-content')
    button_text = get_button.text
    button_link = get_button.attrs['href']
    if (button_text.startswith('Buy eBook - $') or button_text.startswith('EBOOK FROM $')):
        buy_link = convert_google_redirect_to_direct_link(button_link)
        if button_text.startswith('Buy eBook - $'):
            price_str = button_text[12:]
        else:
            price_str = button_text[11:]
        price = money_to_dec(price_str)
        print_link_div = soup.find('div', id='buy_v')
        print_link_href = print_link_div.find('a', id='get-all-sellers-link')
        print_link = print_link_href.attrs['href']
        array = extract_google_books_price_list_from_redirect_link(print_link)
        option = PurchaseOption()
        option.link = buy_link
        option.price = price
        option.seller = 'Google Play'
        option.book_type = 'eBook'
        option.is_rental = False
        option.purchaseID = ''
        array.append(option)
    elif button_text=='Get print book':
        array = extract_google_books_price_list_from_link(button_link)
    elif button_text=='View eBook':
        print_link_div = soup.find('div', id='buy_v')
        print_link_href = print_link_div.find('a', id='get-all-sellers-link')
        print_link = print_link_href.attrs['href']
        array = extract_google_books_price_list_from_redirect_link(print_link)
        # recursively call this function, because the given link should go to a similar page
        array2 = extract_google_books_prices_from_page_link(button_link)
        array.extend(array2)
    else:
        array = []
    return array


def get_google_books_for_isbn(isbn):
    link = get_google_books_page_link_for_isbn(isbn)
    return extract_google_books_prices_from_page_link(link)





print get_google_books_for_isbn('3540417818')
