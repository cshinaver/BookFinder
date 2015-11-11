from flask import render_template, request, flash, redirect, url_for
from flask.views import View
from bookfinder import app
from bookfinder.api.scraper import get_book_object_list_for_book_title
from bookfinder.purchase.form import SellBookForm
from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice
from flask.ext.login import current_user


class SellBook(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = SellBookForm()
        if request.method == 'POST':
            ISBN = request.form['ISBN']
            Price = request.form['Price']

            errors = self.form_error_checking(isbn=ISBN, price=Price)
            if errors:
                return self.redirect_to_self_with_errors(errors)

            temp_book_ls, errors = self.get_book_from_isbn(isbn=ISBN)
            if errors:
                return self.redirect_to_self_with_errors(errors)

            errors = self.create_and_store_purchase_option(
                temp_book=temp_book_ls[0],
                isbn=ISBN,
                price=Price,
            )
            if errors:
                return self.redirect_to_self_with_errors(errors)

            flash('Your book has been logged into the database!', 'success')
            return self.redirect_to_self()
        else:
            return render_template(
                'purchase/purchase_index.html',
                form=form,
            )

    def create_and_store_purchase_option(self, temp_book, isbn, price):
        errors = []
        # Check if book has correct ISBN
        # Check DB for duplicate isbn entry.
        # If so just make purchase option

        book = Book.get(isbn=isbn)
        if not book:
            book = Book()
            book.author = temp_book.author
            if temp_book.subtitle is None:
                book.title = temp_book.title
            else:
                book.title = temp_book.title+': ' + temp_book.subtitle
            book.isbn = isbn
            book.save()

        # add purchaseChoice to DB
        p = PurchaseChoice()
        p.book_id = book.id
        p.price = price
        p.type = 'Hardcover'
        p.isRental = False
        p.link = ''  # TODO change to valid link
        p.local_seller_id = current_user.id
        p.isLocalSeller = True
        p.save()
        return errors

    def redirect_to_self(self):
        return redirect(url_for('sell_book'))

    def get_book_from_isbn(self, isbn):
        errors = []
        book = get_book_object_list_for_book_title('isbn:' + isbn)
        if not book:
            errors.append('ISBN is invalid')
        return book, errors

    def form_error_checking(self, isbn, price):
        errors = []
        if isbn == '':
            errors.append('No ISBN entered')
        if price == '':
            errors.append('No price entered')
        len_isbn = len(isbn)
        if len_isbn != 10 and len_isbn != 13:
            errors.append(
                'ISBN has incorrect number of characters. '
                'Please enter ISBN-10 or ISBN-13'
            )
        return errors

    def redirect_to_self_with_errors(self, errors):
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('sell_book'))


app.add_url_rule('/purchase/', view_func=SellBook.as_view('sell_book'))
