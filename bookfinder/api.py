from flask import render_template
from flask import request

from bookfinder import app

import json
from scraper import BookToDict, get_book_object_list_for_book_title


@app.route('/api/books_list/')
def book_query():
    title = request.args.get('title')
    book_list = []
    for book in get_book_object_list_for_book_title(title):
        book_list.append(BookToDict(book))
    json_output = json.dumps(book_list, sort_keys=True, indent=4)
    return json_output
