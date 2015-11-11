import csv

from bookfinder.models.book import Book
from bookfinder.models.purchasechoice import PurchaseChoice
from bookfinder.api.scraper import get_book_object_list_for_book_title
from bookfinder import app

def load_csv():
    f = open('ISBN_data.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        print row

        if len(row) != 0:
        	ISBN_load = row[0]
        	Seller_load = row[1]
        	Price_load = row[2]

        	#add book object
	        b = Book()  #create temp book object
	        temp_arr = get_book_object_list_for_book_title('isbn:'+ISBN_load)
	        if len(temp_arr) ==0:
	            return
	        temp_var = temp_arr[0]
	        b.isbn = temp_var.isbn
	        b.author = temp_var.author[0] #josh will change
	        if(temp_var.subtitle is None):
	        	b.title = temp_var.title  #check if subtitle is null
	        else:
	        	b.title = temp_var.title+': '+temp_var.subtitle  #check if subtitle is null

	        query_book = Book.get(isbn=b.isbn)	#check if Book object is already in DB
	        if not query_book:
	        	b.save()
	        else:
	        	b.id = query_book.id

	        #Make purchase choice
	     	p = PurchaseChoice()
	        p.id = b.id
	        p.price = Price_load #default to 10
	        p.type = 'Hardcover'
	        p.isRental = False
	        p.link = '' # change to valid link
	        p.local_seller_id = Seller_load # change to user once login is created
	        p.isLocalSeller = True

