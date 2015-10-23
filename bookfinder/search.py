from flask import render_template

from bookfinder import app


@app.route('/search/')
def search():
    return render_template('search/index.html')


@app.route('/search/static/js/search.js')
def js_search():
    return render_template('search/static/js/search.js')
