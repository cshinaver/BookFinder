from flask import Flask, render_template, request, flash, redirect
from bookfinder import app
from scraper import get_book_object_for_book_title
from bookfinder.purchase.form import LoginForm
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice


@app.route('/purchase/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        if request.form['ISBN'] == '':
            flash(u'No ISBN entered', 'error')
        if request.form['Price'] == '':
            flash(u"No Price entered", "error")
        if request.form['Title'] == '':
            flash(u"No Title entered", "error")
        if request.form['Author'] == '':
            flash(u"No Author entered", "error")
        else:
            # create book object using ISBN and Price
            ISBN = request.form['ISBN']
            Price = request.form['Price']
            Type = 'Book'
            isRental = False
            Author = request.form['Author']
            Title = request.form['Title']

            # check if book has correct ISBN
            if get_book_object_for_book_title(ISBN) != -1:
                #  add book to DB
                b = Book()
                b.author = Author
                b.title = Title
                b.isbn = ISBN
                b.save()

                # add purchaseChoice to DB
                p = PurchaseChoice()
                p.book_id = b.id
                p.price = Price
                p.type = 'Hardcover'
                p.isRental = False
                p.link = '' # change to valid link
                p.seller = 'Foo Bar Seller' # change to user once login is created
                p.save()
                flash('Your book has been logged into the database. Yeah!!!', 'success')
                return redirect('')
            else:  # book is not valid
                flash('ISBN is invalid', 'error')
    return render_template(  # reference html script
        'purchase/purchase_index.html',
        form=form,
    )
