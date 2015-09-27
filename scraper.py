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


def get_page_for_google_books_book_search(keyword):
    search_string = (
        'https://www.google.com/search?tbm=bks&q='
        '{search_string}'.format(search_string=keyword,)
    )
    return requests.get(search_string).content


def extract_google_books_page_link_from_li(item):
    h3_item = item.find(
        'h3',
        class_='r',
    )
    a_item = h3_item.find('a')
    return a_item.attrs['href']


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
    for item in list_items:
        price_span = item.find('span', class_='price')
        if price_span!=None:
            seller_link_href = item.find('a')
            seller_name = seller_link_href.text
            seller_link_redir = seller_link_href.attrs['href'] 
            seller_link = convert_google_redirect_to_direct_link(seller_link_redir)
            price_text = price_span.text
            price = float(price_text[1:])
            print 'Buy Link:'
            print seller_link
            print 'Seller:'
            print seller_name
            print 'Price:'
            print price


# Sometimes link is a redirect link in google's format.
# This function translates that to a direct link before extracting.
def extract_google_books_price_list_from_redirect_link(redir_link):
    link = convert_google_redirect_to_direct_link(redir_link)
    extract_google_books_price_list_from_link(link)


def extract_google_books_prices_from_page_link(link):
    content = requests.get(link).content
    soup = BeautifulSoup(content)
    get_button = soup.find('a', id='gb-get-book-content')
    button_text = get_button.text
    button_link = get_button.attrs['href']
    if button_text.startswith('Buy eBook - $'):
        buy_link = convert_google_redirect_to_direct_link(button_link)
        price_str = button_text[13:]
        price = float(price_str)
        print 'Buy eBook:'
        print buy_link
        print 'Price:'
        print price
        print_link_div = soup.find('div', id='buy_v')
        print_link_href = print_link_div.find('a', id='get-all-sellers-link')
        print_link = print_link_href.attrs['href']
        print 'Load List:'
        extract_google_books_price_list_from_redirect_link(print_link)
    elif button_text=='Get print book':
        print 'Load List:'
        extract_google_books_price_list_from_link(button_link)
    elif button_text=='View eBook':
        print 'View eBook:'
        # recursively call this function, because the given link should go to a similar page
        extract_google_books_prices_from_page_link(button_link)
    else:
        print 'unrecognized button:'
        print button_text
        print button_link
    #print content
    #print get_button


def get_google_books_book_prices_for_keyword(keyword):
    content = get_page_for_google_books_book_search(keyword)
    soup = BeautifulSoup(content)
    list_items = soup.find_all('li', class_='g')
    for item in list_items:
        link = extract_google_books_page_link_from_li(item)
        extract_google_books_prices_from_page_link(link)


get_google_books_book_prices_for_keyword('compilers')
#print get_amazon_books_for_keyword('compilers')
