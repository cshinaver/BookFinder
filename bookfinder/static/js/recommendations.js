function get_suggestion_list(user_id, count) {
    get_file('/api/recommend_list/?user_id='+user_id+'&number_of_preferences='+count, function(text) {
        book_list = JSON.parse(text);
        var num_books = book_list.length;
        if(num_books) {
            var sorted_books = book_list.sort(function(a,b) {
                return b.value - a.value;
            });
            for(var i = 0; i < num_books; i++) {
                add_suggestion_to_list(sorted_books[i]);
            }
        }
    });
}

function add_suggestion_to_list(book_info) {
    var book_id = book_info.item_id;
    get_file('/api/book_info/?id='+book_id, function(text) {
        if(text!="") {
            var book = JSON.parse(text);
            document.getElementById("recommendations").style.display="block";
            add_item_to_list(book,"recommendation-list");
        }
    });
}
