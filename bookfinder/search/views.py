from flask import render_template

from bookfinder import app


@app.route('/search/')
def search():
    return render_template('search/index.html')
