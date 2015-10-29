from flask import render_template

from bookfinder import app


@app.route('/purchase/')
def home():
    return render_template('index.html')	#reference html script