from flask import render_template, request

from bookfinder import app
from bookfinder.db.connect import execute_sql_query
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice

import json
from scraper import get_book_object_list_for_book_title, get_amazon_books_for_keyword, get_Barnes_book_prices_for_isbn, get_google_books_for_isbn


@app.route('/api/books_list/')
def book_query():
    title = request.args.get('title')
    book_list = []
    for book in get_book_object_list_for_book_title(title):
        book_list.append(book.to_dict())
    json_output = json.dumps(book_list, sort_keys=True, indent=4)
    return json_output


@app.route('/api/used_option_list/')
def used_option_query():
    isbn = request.args.get('isbn')
    option_list = []
    book_query = execute_sql_query(
        "SELECT * FROM Book WHERE isbn='{ISBN}'".format(
            ISBN=isbn
        )
    )
    if len(book_query)==0:#return blank list if this book is not yet in the database
        return '[]'
    book_id = book_query[0]['id']
    query_return = execute_sql_query(
        "SELECT * FROM PurchaseChoice WHERE book_id={book_id}".format(
            book_id=book_id
        )
    )
    for option in query_return:
        option_list.append({
            'seller': option['seller'],
            'price': option['price'],
            'rental': option['isrental'],
            'book_type': option['type'],
            'link': option['link'],
            'purchaseID': option['id']
        })
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output


@app.route('/api/comparison_option_list/')
def comparison_option_query():
    isbn = request.args.get('isbn')
    option_list = []
    amazon_list = get_amazon_books_for_keyword(isbn)
    if amazon_list is None:
        print 'None returned from get_amazon_books_for_keyword'
    else:
        print (
            "   get_amazon_books_for_keyword('{isbn}')"
            " returned {count} result(s)".format(
                isbn=isbn,
                count=len(amazon_list)
            )
        )
        for option in amazon_list:
            option_list.append(option.to_dict())
    barnes_list = get_Barnes_book_prices_for_isbn(isbn)
    if barnes_list is None:
        print 'None returned from get_Barnes_book_prices_for_isbn'
    else:
        print (
            "get_Barnes_book_prices_for_isbn('{isbn}')"
            " returned {count} result(s)".format(
                isbn=isbn,
                count=len(barnes_list)
            )
        )
        for option in barnes_list:
            option_list.append(option.to_dict())
    google_list = get_google_books_for_isbn(isbn)
    if google_list is None:
        print 'None returned from get_google_books_for_isbn'
    else:
        print (
            "      get_google_books_for_isbn('{isbn}')"
            " returned {count} result(s)".format(
                isbn=isbn,
                count=len(google_list)
            )
        )
        for option in google_list:
            option_list.append(option.to_dict())
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output


# DEBUG - add book
# example address: http://localhost:5000/api/debug/add_book/?title=Book_title&isbn=1625847602&author=test_author
@app.route('/api/debug/add_book/')
def add_book():
    new_book = Book()
    new_book.title = request.args.get('title')
    new_book.isbn = request.args.get('isbn')
    new_book.author = request.args.get('author')
    new_book.save()
    return '{id}'.format(id=new_book.id)
#/DEBUG - add book

# DEBUG - add purchase option
# example address: http://localhost:5000/api/debug/add_purchase_option/?price=12.34&type=print&isRental=true&link=http://www.google.com&seller=test_seller_2&book_id=3
@app.route('/api/debug/add_purchase_option/')
def add_purchase_option():
    new_option = PurchaseChoice()
    new_option.price = request.args.get('price')
    new_option.type = request.args.get('type')
    new_option.isRental = request.args.get('isRental')
    new_option.link = request.args.get('link')
    new_option.seller = request.args.get('seller')
    new_option.book_id = request.args.get('book_id')
    new_option.save()
    return '{id}'.format(id=new_option.id)
#/DEBUG - add purchase option
