from flask import render_template

from bookfinder import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def get_static(path):
    return redirect(url_for('static', filename=path))
