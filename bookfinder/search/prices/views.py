from flask import render_template

from bookfinder import app


@app.route('/search/prices/')
def prices():
    return render_template('search/prices/index.html')
