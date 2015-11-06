from flask import Flask, render_template, request, flash, redirect
from bookfinder import app
from bookfinder.api.scraper import get_book_object_for_book_title
from bookfinder.purchase.form import LoginForm
from bookfinder.models.book import Book
from bookfinder.models.base import BaseModel
from bookfinder.models.purchasechoice import PurchaseChoice
from flask.ext.login import current_user, login_required

@app.route('/purchase/', methods=['GET', 'POST'])
@login_required
def home():
    form = LoginForm()
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        ISBN = request.form['ISBN']
        Price = request.form['Price']
        Type = 'Book'
        isRental = False
        Author = request.form['Author']
        Title = request.form['Title']


        if request.form['ISBN'] == '':
            flash(u'No ISBN entered', 'error')
        if request.form['Price'] == '':
            flash(u"No Price entered", "error")
        if request.form['Title'] == '':
            flash(u"No Title entered", "error")
        if request.form['Author'] == '':
            flash(u"No Author entered", "error")
        if get_book_object_for_book_title('isbn:'+ISBN) == -1:
            flash('ISBN is invalid', 'error')
        elif request.form['Author'] != '' and request.form['Title'] != '' and request.form['Price'] != '' and request.form['ISBN'] != '':
            #Check if book has correct ISBN
            #Check DB for duplicate isbn entry. If so just make purchase option
            
            #  add book to DB
            b = Book()
            b.author = Author
            b.title = Title
            b.isbn = ISBN
            if not (Book.get(isbn=ISBN)):    #if get returns true, already book in DB
                b.save()

            # add purchaseChoice to DB
            p = PurchaseChoice()
            p.book_id = b.id
            p.price = Price
            p.type = 'Hardcover'
            p.isRental = False
            p.link = '' # change to valid link
            p.local_seller_id = current_user.id # change to user once login is created
            p.isLocalSeller = True
            p.save()
            flash('Your book has been logged into the database!', 'success')
            return redirect('')
    return render_template(  # reference html script
        'purchase/purchase_index.html',
        form=form,
    )
