import requests
from bs4 import BeautifulSoup


class Book:
    def __init__(self, *args, **kwargs):
        self.link = ''
        self.price = 0
        self.title = ''
        self.book_type = ''
        self.is_rental = False



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



def get_amazon_book_prices_for_keyword(keyword):
    content = get_page_for_amazon_book_search(keyword)
    soup = BeautifulSoup(content)
    list_items = soup.find_all('li', class_='s-result-item celwidget')
    for item in list_items:
        print item.find_all(
            'span',
            class_='a-size-base a-color-price s-price a-text-bold',
        )

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
    list_wrapper_item = soup.find('li', class_='clearer')
    list_items = list_wrapper_item.find_all('li')
    #print list_items
    for item in list_items:
        product_info = item.find('div', class_='product-info')  #get info of book
        if not product_info:
            continue
        item_title = product_info.find('h2')    #get title
        print item_title.get_text()

        item_price = product_info.find('span', class_='price')      #get price
        print item_price.get_text()

        item_type = product_info.find('ul', class_='formats')
        item_type = item_type.find_all('a')[0]
        print item_type.get_text()

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
get_Barnes_book_prices_for_keyword('compilers')
