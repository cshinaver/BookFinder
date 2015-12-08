import csv
import sys

from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice
from bookfinder.api.scraper import get_books_for_book_title_using_google_books
from bookfinder.api.scraper import AmazonScraper
from random import randint
from bookfinder.models.booksviewed import BooksViewed
from bookfinder.login.views import User


def load_csv(filename):
    f = open(filename)
    csv_f = csv.reader(f)
    newUser = "dummyUSER"
    for row in csv_f:
        print row

        if len(row) != 0:
            userID = row[0]
            ISBN_load = row[1]
            class_name = row[2]

            # add book object
            b = Book()  # create temp book object
            query_book = Book.get(
                    isbn=ISBN_load
            )  # check if Book object is already in DB
            if not query_book:
                temp_arr = get_books_for_book_title_using_google_books(
                        'isbn:' + ISBN_load
                        )
                if len(temp_arr) == 0:
                    AZ = AmazonScraper()
                    amazon_dict = AZ.get_amazon_purchase_choices_for_keyword(ISBN_load)
                    if len(amazon_dict) == 0:
                        print "skipping ISBN: "+ISBN_load
                        continue
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

                b.save()    #save book
            else:   #if book in DB, set b.id to id of DB book
                b.id = query_book.id

            # Make purchase choice
            p = PurchaseChoice()
            p.id = b.id
            p.price = randint(55, 250)  # default to 10
            p.type = 'Hardcover'
            p.isRental = False
            p.link = ''  # change to valid link
            p.local_seller_id = userID  # change to user once login is created
            p.isLocalSeller = True
            p.save()

            booksV = BooksViewed()
            if userID[0]=='-':    #if first user in list signified by '-'' sign, create new user
                #print userID[1:]
                newUser = User(username=userID[1:], password=userID[1:]) #password = userID
            booksV.user_id = newUser
            booksV.book_id = b.id
            booksV.save()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Please pass CSV filename to script"
        exit(1)

    filename = sys.argv[1]
    load_csv(filename)
