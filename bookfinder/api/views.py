from flask import request
from flask.views import View

from bookfinder import app
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice
from bookfinder.models.bookfinderuser import BookfinderUser as User

import json
from scraper import (
    AmazonScraper,
    get_Barnes_book_prices_for_isbn,
    get_google_books_for_isbn,
)


@app.route('/api/books_list/')
def book_query():
    title = request.args.get('title')
    amazon_books = AmazonScraper().get_amazon_books_for_keyword(title)
    # Convert all values to strings
    book_list = [
        {key: str(value) for (key, value) in d.iteritems()}
        for d in amazon_books
    ]
    json_output = json.dumps(book_list, sort_keys=True, indent=4)
    return json_output


class UsedOptionList(View):
    def dispatch_request(self):
        option_list = self.get_list_by_isbn(request.args.get('isbn'))
        json_output = json.dumps(option_list, sort_keys=True, indent=4)
        return json_output

    def get_list_by_isbn(self, isbn):
        book_query = Book.get(isbn=isbn)
        # return blank list if this book is not yet in the database
        if book_query is None:
            option_list = []
        elif isinstance(book_query, list):
            # This indicates there are multiple books
            # with the same ISBN number, which shouldn't happen
            option_list = []
            for book in book_query:
                option_list = self.fill_list_by_bookid(option_list, book.id)
        else:
            option_list = self.fill_list_by_bookid([], book_query.id)
        return option_list

    def fill_list_by_bookid(self, option_list, book_id):
        def add_to_list(old_list, option):
            option.price = "{:.2f}".format(float(option.price))
            if option.isLocalSeller:
                local_seller = User.get(id=option.local_seller_id)
                old_list.append({
                    'seller': local_seller.username,
                    'price': option.price,
                    'rental': option.isRental,
                    'book_type': option.type,
                    'link': option.link,
                    'purchaseID': option.id
                })
            else:
                old_list.append({
                    'seller': option.remoteSellerName,
                    'price': option.price,
                    'rental': option.isRental,
                    'book_type': option.type,
                    'link': option.link,
                    'purchaseID': option.id
                })
            return old_list

        query_return = PurchaseChoice.get(book_id=book_id)
        if isinstance(query_return, list):
            for option in query_return:
                option_list = add_to_list(option_list, option)
        else:
            option_list = add_to_list(option_list, query_return)
        return option_list


@app.route('/api/comparison_option_list/')
def comparison_option_query():
    isbn = request.args.get('isbn')
    option_list = []
    amazon_list = AmazonScraper().get_amazon_purchase_choices_for_keyword(isbn)
    option_list.extend(amazon_list)
    barnes_list = get_Barnes_book_prices_for_isbn(isbn)
    if barnes_list is not None:
        for option in barnes_list:
            option_list.append(option.to_dict())
    google_list = get_google_books_for_isbn(isbn)
    if google_list is not None:
        for option in google_list:
            option_list.append(option.to_dict())
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output

app.add_url_rule(
    '/api/used_option_list/',
    view_func=UsedOptionList.as_view('used_option_list'),
)
