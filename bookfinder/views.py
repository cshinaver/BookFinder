from flask import render_template, send_from_directory

from bookfinder import app
from bookfinder.models.book import Book
from bookfinder.db.connect import execute_sql_query


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recently_viewed_books')
def recently_viewed_books():
    # Get books only
    ls = execute_sql_query(
        """
            select distinct on (book_id) * from purchasechoice
            inner join book on (book.id = purchasechoice.book_id);
        """
    )
    books = []
    for b in ls:
        book = Book()
        book.title = b[-3]
        book.author = b[-1]
        books.append(book)
    return render_template('recently_viewed_books.html', books=books)


@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)
