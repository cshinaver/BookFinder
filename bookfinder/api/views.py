from flask import render_template, request

from bookfinder import app
from bookfinder.db.connect import execute_sql_query

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
    #option_list = []
    #query_return = execute_sql_query('SELECT * FROM PurchaseChoice')
    #for option in query_return:
    #    option_list.append({
    #        'seller': option['seller'],
    #        'price': option['price'],
    #        'rental': option['isRental'],
    #        'book_type': option['type'],
    #        'link': option['link'],
    #        'purchaseID': option['id']
    #    })
    option_list = [{
        'seller': 'seller_1',
        'price': '10.24',
        'rental': False,
        'book_type': 'print',
        'link': '/option?ID=1234',
        'purchaseID': '1234'
        },{
        'seller': 'seller_2',
        'price': '20.48',
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
@app.route('/api/debug/add_book/')
def add_book():
    print execute_sql_query(
        "INSERT INTO Book (id, title, ISBN, author)"
        "VALUES ('{id}', '{title}', '{ISBN}', '{author}')".format(
            id = request.args.get('id'),
            title = request.args.get('title'),
            ISBN = request.args.get('ISBN'),
            author = request.args.get('author')
        )
    )
    return 'success!'
#/DEBUG - add book

# DEBUG - add purchase option
@app.route('/api/debug/add_purchase_option/')
def add_purchase_option():
    print execute_sql_query(
        "INSERT INTO PurchaseChoice (id, price, type, isRental, link, seller, book_id)"
        "VALUES ('{id}', '{price}', '{type}', '{isRental}', '{link}', '{seller}', '{book_id}')".format(
            id = request.args.get('id'),
            price = request.args.get('price'),
            type = request.args.get('type'),
            isRental = request.args.get('isRental'),
            link = request.args.get('link'),
            seller = request.args.get('seller'),
            book_id = request.args.get('book_id')
        )
    )
    return 'success!'
#/DEBUG - add purchase option
