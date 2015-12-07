function get_suggestion_list(user_id, count) {
    get_file('/api/recommend_list/?user_id='+user_id+'&number_of_preferences='+count, function(text) {
        book_list = JSON.parse(text);
        var num_books = book_list.length;
        if(num_books) {
            for(var i = 0; i < num_books; i++) {
                add_suggestion_to_list(book_list[i]);
            }
        }
    });
}

function add_suggestion_to_list(book_info) {
    var book_id = book_info.item_id;
    get_file('/api/book_info/?id='+book_id, function(text) {
        if(text!="") {
            var book_data = JSON.parse(text);
            var isbn = book_data.isbn;
            get_file('/api/books_list/?title=isbn:'+isbn, function(text) {
                var book_list = JSON.parse(text);
                if(book_list.length) {
                    var book = book_list[1];
                    document.getElementById("recommendations").style.display="block";
                    add_item_to_list(book,"recommendation-list");
                }
            });
        }
    });
}
