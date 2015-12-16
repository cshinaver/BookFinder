function add_item_to_list(book, list_id) {
    var new_entry = document.createElement("a");
    //thumbnail:
    var new_thumb_frame = document.createElement("div");
    var new_thumb = document.createElement("img");
    new_thumb.setAttribute("src",book.thumbnail_link);
    new_thumb_frame.appendChild(new_thumb);
    new_thumb_frame.setAttribute("style","float:left;padding-right:10px;");
    new_entry.appendChild(new_thumb_frame);
    //info:
    var new_info_frame = document.createElement("div");
    //title:
    var new_title = document.createElement("h4");
    var new_title_text = document.createTextNode(book.title);
    new_title.appendChild(new_title_text);
    new_title.setAttribute("class","list-group-item-heading");
    new_info_frame.appendChild(new_title);
    //isbn:
    var new_isbn = document.createElement("p");
    var new_isbn_text = document.createTextNode("ISBN: "+book.isbn);
    new_isbn.appendChild(new_isbn_text);
    new_isbn.setAttribute("class","list-group-item-text");
    new_info_frame.appendChild(new_isbn);
    //Author:
    var authors=book.authors.replace("\', u\'", ", ");  //format string if multiple authors
    var new_author = document.createElement("p");
    var new_author_text = document.createTextNode("Author: "+authors.slice(3,authors.length-2));//cut off ugly format of author string
    new_author.appendChild(new_author_text);
    new_author.setAttribute("class","list-group-item-text");
    new_info_frame.appendChild(new_author);
    //Book_type:
    var new_book_type = document.createElement("p");
    var new_book_type_text = document.createTextNode("Book Type: "+book.book_type);
    new_book_type.appendChild(new_book_type_text);
    new_book_type.setAttribute("class","list-group-item-text");
    new_info_frame.appendChild(new_book_type);
    new_entry.appendChild(new_info_frame);
    new_entry.setAttribute("style","overflow:auto;");
    new_entry.setAttribute("class","list-group-item");
    new_entry.setAttribute("href",'/search/prices?isbn=' + book.isbn);
    document.getElementById(list_id).appendChild(new_entry);
}
