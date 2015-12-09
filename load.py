import csv
import sys
from uuid import uuid4

from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice
from bookfinder.api.scraper import get_books_for_book_title_using_google_books
from bookfinder.api.scraper import AmazonScraper
from random import randint
from bookfinder.models.booksviewed import BooksViewed
from bookfinder.login.views import User


def store_book_info_for_user_and_isbn(user_id, isbn, isbns_to_retry):
    # add book object
    b = Book()  # create temp book object
    query_book = Book.get(
        isbn=isbn
    )  # check if Book object is already in DB
    if not query_book:
        #temp_arr = get_books_for_book_title_using_google_books(
        #    'isbn:' + isbn
        #)
        temp_arr = []
        if len(temp_arr) == 0:
            AZ = AmazonScraper()
            amazon_dict = AZ.get_amazon_purchase_choices_for_keyword(isbn)
            if len(amazon_dict) == 0:
                isbn_info = {}
                isbn_info['isbn'] = isbn
                isbn_info['user_id'] = user_id
                isbn_info['retries'] = 0
                isbns_to_retry.append(isbn_info)
                return False
            temp_book = Book()
            temp_book.isbn = amazon_dict[0].get('isbn')
            temp_book.title = amazon_dict[0].get('title')
            temp_book.author = amazon_dict[0].get('author')
            temp_book.thumbnail_link = amazon_dict[0].get('thumbnail_link')
            temp_book.subtitle = ''
            temp_arr.append(temp_book)

        temp_var = temp_arr[0]
        b.isbn = temp_var.isbn
        b.author = temp_var.author
        if(temp_var.subtitle is None):
            b.title = temp_var.title  # check if subtitle is null
        else:
            b.title = (
                temp_var.title +
                ': ' + temp_var.subtitle  # check if subtitle is null
            )
        b.thumbnail_link = temp_var.thumbnail_link

        # Sometimes, the isbn found by the scraper differs from the one
        # in the file
        # In this case, a duplicate book would be created (same isbn)
        # Check for found isbn first before saving book
        possible_duplicate_book = Book.get(isbn=b.isbn)
        if possible_duplicate_book:
            b = possible_duplicate_book
        else:
            b.save()  # save book

    else:  # if book in DB, set b.id to id of DB book
        b.id = query_book.id

    # Make purchase choice
    p = PurchaseChoice()
    p.id = b.id
    p.price = randint(55, 250)  # default to 10
    p.type = 'Hardcover'
    p.isRental = False
    p.link = ''  # change to valid link
    p.local_seller_id = user_id  # change to user once login is created
    p.isLocalSeller = True
    p.save()

    booksV = BooksViewed()
    booksV.user_id = user_id
    booksV.book_id = b.id
    booksV.save()
    return True


def load_csv(filename):
    f = open(filename)
    csv_f = csv.reader(f)
    newUser = "dummy"
    current_user_id = None
    current_row_id = None
    # keep track of isbns to retry
    isbns_to_retry = []
    for row in csv_f:
        if len(row) != 0:
            print row
            row_id = row[0]
            isbn = row[1]
        else:
            continue

        # Same user for given set of lines
        if current_row_id != row_id:
            newUser = User(username=str(uuid4())[:20], password="test")
            newUser.save()
            current_user_id = newUser.id
            current_row_id = row_id

        store_book_info_for_user_and_isbn(
            current_user_id,
            isbn,
            isbns_to_retry,
        )

    # retry failed isbns
    failed_isbns = []
    while isbns_to_retry:
        max_retries = 5

        success = False
        isbn_info = isbns_to_retry[0]
        for i in xrange(0, max_retries):
            success = store_book_info_for_user_and_isbn(
                isbn_info['user_id'],
                isbn_info['isbn'],
                []
            )
            if success:
                break
        if not success:
            failed_isbns.append(isbn_info['isbn'])

        isbns_to_retry = isbns_to_retry[1:]
    for isbn in failed_isbns:
        print isbn + " failed"

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Please pass CSV filename to script"
        exit(1)

    filename = sys.argv[1]
    load_csv(filename)
