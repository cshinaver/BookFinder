from flask import render_template, request, flash, redirect
from bookfinder import app
import scraper
from scraper import get_book_object_for_book_title
from .form import LoginForm

@app.route('/purchase/', methods = ['GET', 'POST'])
def home():
	error = None
	form = LoginForm()
	if request.method == 'POST':
		if request.form['ISBN'] == '':
			flash("No ISBN entered")
			error = 'No ISBN entered'
		elif request.form['Price'] == '':
			flash("No Price entered")
			error = 'No Price entered'
		else:
			flash("Book Submitted")

			#create book object using ISBN and Price
			ISBN = request.form['ISBN']
			Price = request.form['Price']
			Type = 'Book'
			isRental = False;

			#check if book has correct ISBN
			#import ipdb;ipdb.set_trace()
			if(get_book_object_for_book_title(ISBN) != -1):
				#add book to DB
				return redirect('')
			else:	# book is not valid
				error('ISBN is no good')
	return render_template('purchase/purchase_index.html',form=form, error = error)	#reference html script
#	return render("hello")