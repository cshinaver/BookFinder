from flask import render_template, request

from bookfinder import app


@app.route('/search/prices/')
def prices():
    return render_template('search/prices/index.html', args=request.args)
