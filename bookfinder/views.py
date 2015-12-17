from flask import render_template, send_from_directory
import json

from bookfinder import app
from bookfinder.db.connect import execute_sql_query


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recently_viewed_books')
def recently_viewed_books():
    # Get books only
    isbns = execute_sql_query(
        """
            select (isbn) from booksviewed
            inner join book on (book.id = booksviewed.book_id)
            order by time_added desc
            limit 10;
        """
    )
    isbns = [ls[0] for ls in isbns]
    json_isbns = json.dumps(isbns)
    return render_template('recently_viewed_books.html', isbns=json_isbns)


@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)
