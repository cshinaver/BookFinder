function get_option_list(query) {
	get_used_option_list(query);
	get_comparison_option_list(query);
}


function get_used_option_list(query) {
	get_file('/api/used_option_list/?isbn=' + query, function(text) {
		document.getElementById("used-list-body").innerHTML = "";
		document.getElementById("used-list-head").style.display = "";
		option_list = JSON.parse(text);
		var num_options = option_list.length;
		if(num_options) {
			for(var i = 0; i < num_options; i++) {
				add_option_to_list(option_list[i],"used-list-body");
			}
		} else { // doesn't seem to be working
			document.getElementById("used-list").innerHTML = "Sorry. There are no Book results for isbn number " + query + ".";
		}
	});
}


function get_comparison_option_list(query) {
	get_file('/api/comparison_option_list/?isbn=' + query, function(text) {
		document.getElementById("comparison-list-body").innerHTML = "";
		document.getElementById("comparison-list-head").style.display = "";
		option_list = JSON.parse(text);
		var num_options = option_list.length;
		if(num_options) {
			for(var i = 0; i < num_options; i++) {
				add_option_to_list(option_list[i],"comparison-list-body");
			}
		} else { // doesn't seem to be working
			document.getElementById("comparison-list").innerHTML = "Sorry. There are no Book results for isbn number " + query + ".";
		}
	});
}

function fill_search(text) {
	document.getElementById("head-search-bar_text").value = text;
}

function add_option_to_list(option, list_id) {
	var new_row = document.createElement("tr");
	//Seller:
	var new_seller = document.createElement("td");
	var new_seller_link = document.createElement("a");
	var new_seller_text = document.createTextNode(option.seller);
	new_seller_link.setAttribute("href",option.link);
	new_seller_link.setAttribute("style","display:block;width:100%;height:100%;padding:10px;text-decoration:none;color:black;");
	new_seller_link.appendChild(new_seller_text);
	new_seller.appendChild(new_seller_link);
	new_seller.setAttribute("style","padding:0px;");
	new_row.appendChild(new_seller);
	//Type:
	var new_type = document.createElement("td");
	var new_type_link = document.createElement("a");
	var new_type_text = document.createTextNode(option.book_type);
	new_type_link.setAttribute("href",option.link);
	new_type_link.setAttribute("style","display:block;width:100%;height:100%;padding:10px;text-decoration:none;color:black;");
	new_type_link.appendChild(new_type_text);
	new_type.appendChild(new_type_link);
	new_type.setAttribute("style","padding:0px;");
	new_row.appendChild(new_type);
	//Rental:
	var new_rental = document.createElement("td");
	var new_rental_link = document.createElement("a");
	var new_rental_text = document.createTextNode(option.rental);
	new_rental_link.setAttribute("href",option.link);
	new_rental_link.setAttribute("style","display:block;width:100%;height:100%;padding:10px;text-decoration:none;color:black;");
	new_rental_link.appendChild(new_rental_text);
	new_rental.appendChild(new_rental_link);
	new_rental.setAttribute("style","padding:0px;");
	new_row.appendChild(new_rental);
	//Price:
	var new_price = document.createElement("td");
	var new_price_link = document.createElement("a");
	var new_price_text = document.createTextNode(option.price);
	new_price_link.setAttribute("href",option.link);
	new_price_link.setAttribute("style","display:block;width:100%;height:100%;padding:10px;text-decoration:none;color:black;");
	new_price_link.appendChild(new_price_text);
	new_price.appendChild(new_price_link);
	new_price.setAttribute("style","padding:0px;");
	new_row.appendChild(new_price);
	new_row.setAttribute("class","active");
	document.getElementById(list_id).appendChild(new_row);
}
