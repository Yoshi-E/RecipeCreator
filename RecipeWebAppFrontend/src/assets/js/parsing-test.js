//Text changed
jQuery("#editor").on('input', debounce(
	function(e) {
			if(e.target.blocking == true) {
				return 0;
			}
			e.target.blocking = true;
			//e.target.innerText = e.target.innerText.normalize('NFKC');
			payload = { type: "recipe_text_updated", 
						recipe_text: e.target.innerText
					};
			post_json(payload, handel_json, handel_error);
		}, 100)
	);
	

// defaults
var options = {
	className: 'cehighlighter',
	elastic: true, // let the contenteditable grow with the content.
    regexs: [
        { pattern: /(^|\s)(#[a-z\d-]+)/gi, template: '$1<span class="hashtag">$2</span>' },
        { pattern: /((https?):\/\/[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:/~+#-]*[\w@?^=%&amp;/~+#-])?)/gi, template: '<span class="url">$1</span>' },
        { pattern: /(@([a-z\d_]+))/gi, template: '<span class="mention">$1</span>' }
    ]
}

//var el = document.querySelector('#editor'); 
//var highlighter = new CEHighlighter(el);


function handel_error(e) {
	document.getElementById("editor").blocking = false;
}


function handel_json(json) {
	var list = json["data"];
	console.log(list);
	document.getElementById("editor").blocking = false;
	
	//Create overview Table
	//build pattern list:
	tbl = document.getElementById("searchTable");
	while ( tbl.rows.length > 0 ) {
		tbl.deleteRow(0);
	}
	if (list !== null) {
		//Create header:
		var tr = tbl.insertRow();
		["value", "unit", "ingredient", "original"].forEach(function(entry) {
			var td = tr.insertCell();
			td.appendChild(document.createTextNode(entry));
		});
		//Create Body
		list.forEach(function(entry) {
			var tr = tbl.insertRow();
			["value", "unit", "ingredient", "original"].forEach(function(field) {
				var td = tr.insertCell();
				var text = entry[field]
				if(entry[field] == null) {
					text = "";
				};
				td.appendChild(document.createTextNode(text));
				td.style.border = '1px solid black';
				td.style.backgroundColor = getColorForPercentage(entry["confidence"]);
			});	
		});
	}
	
	//For each we calculated the correct value
	var sum_dict = new Object();
	list.forEach(function(entry) {
		var dict = new Object();
		if(entry["data"]) {
			for (const [key, value] of Object.entries(entry["data"])) {
				dict[key] = 0;
				if(value > 0) {
					dict[key] = value/100 * entry["value"];
				}
				if(sum_dict[key]) {
					sum_dict[key] += dict[key];
				} else {
					sum_dict[key] = dict[key];
				}
			};
		}
		entry["calculated"] = dict;
	});
	console.log();
	
	tbl = document.getElementById("resultTable");
	while ( tbl.rows.length > 0 ) {
		tbl.deleteRow(0);
	}
	//Create header:
	var tr = tbl.insertRow();
	var td = tr.insertCell();
	td.appendChild(document.createTextNode(""));
	for(const [key, value] of Object.entries(json["column_map"])) {
		var td = tr.insertCell();
		td.appendChild(document.createTextNode(value.replace('/100g', '')));
	}
	
	//Row 1
	var tr = tbl.insertRow();
	var td = tr.insertCell();
	td.appendChild(document.createTextNode("Summe"));
	for (const [key, value] of Object.entries(json["column_map"])) {
		var td = tr.insertCell();
		td.appendChild(document.createTextNode(Math.round((sum_dict[key] + Number.EPSILON) * 100) / 100));
		td.style.border = '1px solid black';
	}
	//Row 2
	var tr = tbl.insertRow();
	portion = document.getElementById("portionen").value;
	var td = tr.insertCell();
	td.appendChild(document.createTextNode("Portion ("+portion+")"));
	for (const [key, value] of Object.entries(json["column_map"])) {
		var td = tr.insertCell();
		td.appendChild(document.createTextNode(Math.round((sum_dict[key]/portion + Number.EPSILON) * 100) / 100));
		td.style.border = '1px solid black';
	}
}
