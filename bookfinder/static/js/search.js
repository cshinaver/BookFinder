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
	var new_entry = document.createElement("a");
	//thumbnail:
	var new_thumb_frame = document.createElement("div");
	var new_thumb = document.createElement("img");
	new_thumb.setAttribute("src",book.Thumbnail_link);
	new_thumb_frame.appendChild(new_thumb);
	new_thumb_frame.setAttribute("style","float:left;padding-right:10px;");
	new_entry.appendChild(new_thumb_frame);
	//info:
	var new_info_frame = document.createElement("div");
	//title:
	var new_title = document.createElement("h4");
	var new_title_text = document.createTextNode(book.Title);
	new_title.appendChild(new_title_text);
	new_title.setAttribute("class","list-group-item-heading");
	new_info_frame.appendChild(new_title);
	//subtitle:
	var new_subtitle = document.createElement("p");
	var new_subtitle_text = document.createTextNode(book.Subtitle);
	new_subtitle.appendChild(new_subtitle_text);
	new_subtitle.setAttribute("class","list-group-item-text");
	new_info_frame.appendChild(new_subtitle);
	//isbn:
	var new_isbn = document.createElement("p");
	var new_isbn_text = document.createTextNode(book.isbn);
	new_isbn.appendChild(new_isbn_text);
	new_isbn.setAttribute("class","list-group-item-text");
	new_info_frame.appendChild(new_isbn);
	new_entry.appendChild(new_info_frame);
	new_entry.setAttribute("style","overflow:auto;");
	new_entry.setAttribute("class","list-group-item");
	new_entry.setAttribute("href",'/search/prices?isbn=' + book.isbn);
	document.getElementById("result-list").appendChild(new_entry);
}
