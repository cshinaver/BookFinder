from flask import render_template, send_from_directory

from bookfinder import app
from bookfinder.models.book import Book


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all_books')
def all_books():
    books = Book.all()
    return render_template('all_books.html', books=books)


@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)
