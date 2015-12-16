function get_book_list(query) {
    function get_book_list_helper(retries) {
        var max_retries = 5;
        get_file('/api/books_list/?title=' + query, function(text) {
            document.getElementById("result-list").innerHTML = "";
            book_list = JSON.parse(text);
            var num_books = book_list.length;
            if(num_books) {
                for(var i = 0; i < num_books; i++) {
                    add_book_to_list(book_list[i]);
                }
            }
            else if (retries < max_retries) {
                retries += 1;
                get_book_list_helper(retries);
            } else {
                document.getElementById("result-list").innerHTML = "Sorry. There are no Book results for the search query \"" + query + "\".";
            }
        });
    }
    get_book_list_helper(0);
}

function fill_search(text) {
    document.getElementById("main-search-bar_text").value = text;
}

function add_book_to_list(book) {
    add_item_to_list(book,"result-list");
}
