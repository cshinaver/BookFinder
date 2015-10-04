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
        # http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias
        # %3Daps&field-keywords=compilers
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
        # http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias
        # %3Daps&field-keywords=compilers
    )
    return requests.get(search_string).content

def get_Barnes_book_prices_for_keyword(keyword):
    content = get_page_for_Barnes_book_search(keyword)
    soup = BeautifulSoup(content)
    if soup.find('li', class_='clearer'):
        list_wrapper_item = soup.find('li', class_='clearer')
        list_items = list_wrapper_item.find_all('li')
        list_PurchaseOptions = []
        for item in list_items:
            new_PurchaseOption = PurchaseOption()
            product_info = item.find('div', class_='product-info')  #get info of book
            if not product_info:
                continue
            item_url_extension = product_info.find('h2').find('a').attrs['href']
            item_base = "http://www.barnesandnoble.com"
            item_url = item_base+item_url_extension
            new_PurchaseOption.link = item_url          #get link

            new_PurchaseOption.is_rental = 'false' #isRental
            new_PurchaseOption.purchaseID = ''

            item_price = product_info.find('span', class_='price')      #get price
            new_PurchaseOption.price = item_price.get_text()

            item_type = product_info.find('ul', class_='formats')       #get book type
            item_type = item_type.find_all('a')[0]
            new_PurchaseOption.book_type = item_type.get_text()

            new_PurchaseOption.seller = 'Barnes and Noble'  #seller

            if new_PurchaseOption:      #if purchaseoption exists, add to list
                list_PurchaseOptions.append(new_PurchaseOption)
        return list_PurchaseOptions
    else:
        print "No results found at 'http://www.barnesandnoble.com' for '%s'" %keyword



def get_page_for_Chegg_book_search(keyword):
    search_string = (
        'http://www.chegg.com/search/{search_string}/'
        'federated?trackid=2ad2613f&strackid=520dd664&event=enter_submit#p=1'.format(
            search_string=keyword,

            # http://www.chegg.com/search/compilers/
            # federated?trackid=07041517&strackid=4105f5f3&event=enter_submit#p=1

            # http://www.chegg.com/search/data%20structures%20c%2B%2B/
            # federated?trackid=57ae47c4&strackid=187a3a14&event=enter_submit#p=1

            # http://www.chegg.com/search/database/
            # federated?trackid=2b4f7cbb&strackid=3596f6c9&event=enter_submit#p=1


        )
    )
    return requests.get(search_string).content


def get_Chegg_book_prices_for_keyword(keyword):
    #content = get_page_for_Chegg_book_search(keyword)
    content = requests.get("http://www.chegg.com/search/compilers/federated?trackid=66da70d5&strackid=170c806a&event=enter_submit#p=1").content
    print content
    soup = BeautifulSoup(content)
    import ipdb; ipdb.set_trace()
    list_items = soup.find_all('li', class_='item-result Chgsec_ls')
    print 'Chegg items: '
    for item in list_items:
        #print 'loop'
        #print item
        print item.find_all(
            'span',
            class_='price',
        )


#get_amazon_book_prices_for_keyword('compilers')
#get_Chegg_book_prices_for_keyword('compilers')
print get_Barnes_book_prices_for_keyword('48391750341')
