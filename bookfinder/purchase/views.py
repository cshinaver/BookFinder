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


        if ISBN == '':
            flash(u'No ISBN entered', 'error')
        if len(ISBN) != 13:
            flash('ISBN needs to be 13 characters long', 'error') 
        if Price == '':
            flash(u"No Price entered", "error")
        if Title == '':
            flash(u"No Title entered", "error")
        if Author == '':
            flash(u"No Author entered", "error")
        if get_book_object_for_book_title('isbn:'+ISBN) == -1:
            flash('ISBN is invalid', 'error')
        elif Author != '' and Title != '' and Price != '' and ISBN != '' and len(ISBN) == 13:
            #Check if book has correct ISBN
            #Check DB for duplicate isbn entry. If so just make purchase option
            
            #  add book to DB
            b = Book()
            b.author = Author
            b.title = Title
            b.isbn = ISBN

            temp_book_item = Book.get(isbn=ISBN)
            if not (temp_book_item):    #if get returns true, already book in DB
                b.save()
            else:
                b.id = temp_book_item.id

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
