from flask import render_template, request

from bookfinder import app
from bookfinder.db.connect import execute_sql_query
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice

import json
from scraper import (
    get_book_object_list_for_book_title,
    get_amazon_books_for_keyword,
    get_Barnes_book_prices_for_isbn,
    get_google_books_for_isbn,
)


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
    def get_list_by_isbn(isbn):
        def fill_list_by_bookid(option_list,book_id):
            def add_to_list(old_list,option):
                if option.isLocalSeller:
                    old_list.append({
                        'seller': option.local_seller_id,
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
            if isinstance(book_query,list):
                for option in query_return:
                    option_list = add_to_list(option_list,option)
            else:
                option_list = add_to_list(option_list,query_return)
            return option_list
        
        book_query = Book.get(isbn=isbn)
        if book_query is None:#return blank list if this book is not yet in the database
            option_list = []
        elif isinstance(book_query,list):
            # This indicates there are multiple books with the same ISBN number, which shouldn't happen
            option_list = []
            for book in book_query:
                option_list = fill_list_by_bookid(option_list,book.id)
        else:
            option_list = fill_list_by_bookid([],book_query.id)
        return option_list
    
    option_list = get_list_by_isbn(request.args.get('isbn'))
    json_output = json.dumps(option_list, sort_keys=True, indent=4)
    return json_output


@app.route('/api/comparison_option_list/')
def comparison_option_query():
    isbn = request.args.get('isbn')
    option_list = []
    amazon_list = get_amazon_books_for_keyword(isbn)
    if amazon_list is not None:
        for option in amazon_list:
            option_list.append(option.to_dict())
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
