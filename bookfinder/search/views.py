from flask import render_template, request, make_response

from bookfinder import app


@app.route('/search/')
def search():
    return render_template('search/index.html', args=request.args)


@app.route('/search/prices/')
def prices():
    isbn = request.args.get('isbn')
    resp = make_response(
        render_template('search/price-comparison.html', isbn=isbn)
    )
    resp.set_cookie('isbn', isbn)
    return resp
