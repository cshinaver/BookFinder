import requests
from bs4 import BeautifulSoup

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

def get_page_for_Barnes_book_search(keyword):
    search_string = (
        'http://www.barnesandnoble.com/s/{search_string}?fs=0&_requestid=284459'.format(
            search_string=keyword,
        )
    )
    return requests.get(search_string).content

def get_Barnes_book_prices_for_keyword(keyword):
    content = get_page_for_Barnes_book_search(keyword)
    soup = BeautifulSoup(content)
    soup.find('div', class_='header')
    if soup.find('section', id='prodSummary'):
        new_PurchaseOption = PurchaseOption()
        list_wrapper_item = soup.find('section', id='prodSummary')
        product_info = list_wrapper_item.find('li', class_='tab selected')
        #print list_wrapper_item
        #product_info = list_wrapper_item.find('section', id='prodSummary')  #get info of book
        #print list_wrapper_item
        #print product_info.find_all('a')[0]
        item_url_extension = (product_info.find_all('a')[0]).attrs['href']
        item_base = "http://www.barnesandnoble.com"
        item_url = item_base+item_url_extension
        new_PurchaseOption.link = item_url          #get link
        #print item_url

        new_PurchaseOption.is_rental = False #isRental
        new_PurchaseOption.purchaseID = ''

        item_price = product_info.find_all('a')[1]     #get price
        new_PurchaseOption.price = item_price.get_text()

        #item_type = product_info.find('ul', class_='formats')       #get book type
        item_type = product_info.find_all('a')[0]
        new_PurchaseOption.book_type = item_type.get_text()

        new_PurchaseOption.seller = 'Barnes and Noble'  #seller

        return new_PurchaseOption
    else:
        print "No results found at 'http://www.barnesandnoble.com' for '%s'" %keyword



def get_page_for_Chegg_book_search(keyword):
    search_string = (
        'http://www.chegg.com/search/{search_string}/'
        'federated?trackid=2ad2613f&strackid=520dd664&event=enter_submit#p=1'.format(
            search_string=keyword,

        )
    )
    return requests.get(search_string).content
