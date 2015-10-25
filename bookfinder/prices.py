from flask import render_template

from bookfinder import app


@app.route('/prices/')
def prices():
    return render_template('prices/index.html')


@app.route('/prices/static/js/prices.js')
def js_prices():
    return render_template('prices/static/js/prices.js')
