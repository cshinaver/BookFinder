from flask import Flask, render_template, request, flash, redirect
from bookfinder import app
from scraper import get_book_object_for_book_title
from bookfinder.purchase.form import LoginForm
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice


@app.route('/purchase/', methods=['GET', 'POST'])
def home():
    error = None
    form = LoginForm()
    #import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        if request.form['ISBN'] == '':
            flash("No ISBN entered")
            error = 'No ISBN entered'
        elif request.form['Price'] == '':
            flash("No Price entered")
            error = 'No Price entered'
        else:
            flash("Book Submitted")
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
                type = 'Hardcover'
                isRental = False
                link = '' # change to valid link
                seller = 'Foo Bar Seller' # change to user once login is created
                p.save()

                return redirect('')
            else:  # book is not valid
                error = 'ISBN is no good'
    return render_template(  # reference html script
        'purchase/purchase_index.html',
        form=form,
        error=error,
    )
