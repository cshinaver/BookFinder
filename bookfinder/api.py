from flask import render_template
from flask import request

from bookfinder import app

import json
from scraper import Book_to_dict, get_book_object_list_for_book_title, PurchaseOption_to_dict, get_amazon_books_for_keyword, get_Barnes_book_prices_for_isbn, get_google_books_for_isbn


@app.route('/api/books_list/')
def book_query():
    title = request.args.get('title')
    book_list = []
    for book in get_book_object_list_for_book_title(title):
        book_list.append(Book_to_dict(book))
    json_output = json.dumps(book_list, sort_keys=True, indent=4)
    return json_output


@app.route('/api/used_option_list/')
def used_option_query():
    isbn = request.args.get('isbn')
    #option_list = []
    #for option in get_google_books_for_isbn(isbn):
    #    option_list.append(PurchaseOption_to_dict(option))
    option_list = [{
        'seller': 'seller_1',
        'price': 10.24,
        'rental': False,
        'book_type': 'print',
        'link': '/option?ID=1234',
        'purchaseID': '1234'
        },{
        'seller': 'seller_2',
        'price': 20.48,
        'rental': True,
        'book_type': 'eBook',
        'link': '/option?ID=5678',
        'purchaseID': '5678'
        }]
    #
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output


@app.route('/api/comparison_option_list/')
def comparison_option_query():
    isbn = request.args.get('isbn')
    option_list = []
    for option in get_amazon_books_for_keyword(isbn):
        option_list.append(PurchaseOption_to_dict(option))
    for option in get_Barnes_book_prices_for_isbn(isbn):
        option_list.append(PurchaseOption_to_dict(option))
    for option in get_google_books_for_isbn(isbn):
        option_list.append(PurchaseOption_to_dict(option))
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output
