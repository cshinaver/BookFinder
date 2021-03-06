from flask import request
from flask.ext.login import (
    current_user,
)
from flask.views import View
from isbnlib import to_isbn13

from bookfinder import app
from bookfinder.models.book import Book
from bookfinder.models.booksviewed import BooksViewed
from bookfinder.models.purchasechoice import PurchaseChoice
from bookfinder.models.bookfinderuser import BookfinderUser as User

import json
import requests
from scraper import (
    AmazonScraper,
    get_Barnes_book_prices_for_isbn,
    get_books_for_book_title_using_google_books,
    get_google_books_for_isbn,
)


@app.route('/api/book_for_isbn/')
def book_for_isbn():
    isbn = request.args.get('isbn')
    isbn = to_isbn13(isbn)
    amazon_books = AmazonScraper().get_amazon_books_for_keyword(isbn)
    # Convert all values to strings
    book_list = [
        {key: value for (key, value) in d.iteritems()}
        for d in amazon_books
    ]
    json_output = json.dumps(book_list[0], sort_keys=True, indent=4)
    return json_output


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


@app.route('/api/recommend_list/')
def recommend_list():
    number_of_preferences = request.args.get('number_of_preferences')
    user_id = request.args.get('user_id')
    engine_url = app.config['RECOMMENDATION_ENGINE_URL']
    r = requests.post(
        "{engine_url}/get-recommendation".format(engine_url=engine_url),
        data={
            "user_id": user_id,
            "number_of_preferences": number_of_preferences
        },
    )
    return r.content, r.status_code


@app.route('/api/book_info/')
def book_info():
    id = request.args.get('id')
    book_data = Book.get(id=id)
    if book_data is None:
        return ""
    json_output = json.dumps(book_data.__dict__, sort_keys=True, indent=4)
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
            if not option:
                return old_list
            elif not option.price:
                return old_list
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


@app.route('/api/set_user_recommendation/', methods=['POST'])
def set_user_recommendation():
    """
    params: book_isbn
    """
    user_id = current_user.id
    book_isbn = request.form.get('book_isbn')
    book = Book.get(isbn=book_isbn)

    if not book:
        book = Book()
        # First try amazon scraper
        amazon_books = AmazonScraper().get_amazon_books_for_keyword(
            book_isbn,
        )
        if not amazon_books:
            # use google books if not amazon
            google_books = get_books_for_book_title_using_google_books(
                book_isbn,
            )
            if not google_books:
                return 'Book could not be found', 500
            google_book = google_books[0]
            book.title = google_book.title
            book.author = google_book.author
            book.isbn = to_isbn13(google_book.isbn)
            book.thumbnail_link = google_book.thumbnail_link
        else:
            amazon_book = amazon_books[0]
            book.isbn = to_isbn13(book_isbn)
            if 'title' in amazon_book:
                book.title = amazon_book['title']
            if 'author' in amazon_book:
                book.author = amazon_book['author']
            if not 'thumbnail_link':
                return 'No thumbnail', 500
            book.thumbnail_link = amazon_book['thumbnail_link']
        book.save()

    existing_bv = BooksViewed.get(user_id=user_id, book_id=book.id)
    if not existing_bv:
        bv = BooksViewed()
        bv.user_id = user_id
        bv.book_id = book.id
        bv.save()
        return 'Book View added successfully', 201

    return 'Book View already exists', 200


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
