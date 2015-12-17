function get_book_list_for_isbn(json_isbns) {
    isbn_list = JSON.parse(json_isbns);
    document.getElementById("result-list").innerHTML = "";
    isbn_list.forEach(function(isbn) {
        get_file('/api/books_list/?title=' + isbn, function(text) {
            book_list = JSON.parse(text);
                add_book_to_list(book_list[0]);
        });
    });
}

function get_book_list(query) {
    get_file('/api/books_list/?title=' + query, function(text) {
        document.getElementById("result-list").innerHTML = "";
        book_list = JSON.parse(text);
        var num_books = book_list.length;
        if(num_books) {
            for(var i = 0; i < num_books; i++) {
                add_book_to_list(book_list[i]);
            }
        } else { // doesn't seem to be working
            document.getElementById("result-list").innerHTML = "Sorry. There are no Book results for the search query \"" + query + "\".";
        }
    });
}

function fill_search(text) {
    document.getElementById("main-search-bar_text").value = text;
}

function add_book_to_list(book) {
    add_item_to_list(book,"result-list");
}
