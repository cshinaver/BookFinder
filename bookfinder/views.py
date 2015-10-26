from flask import render_template, send_from_directory

from bookfinder import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('static', path)
