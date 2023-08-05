function save(filename, data) {
	const blob = new Blob([data], {type: 'text/csv'});
	if(window.navigator.msSaveOrOpenBlob) {
		window.navigator.msSaveBlob(blob, filename);
	}
	else{
		const elem = window.document.createElement('a');
		elem.href = window.URL.createObjectURL(blob);
		elem.download = filename;
		document.body.appendChild(elem);
		elem.click();
		document.body.removeChild(elem);
	}
}

var data = selected_data.data
var csv_out = "";

for (const key of Object.keys(data)) {
	csv_out += key + ","
}
csv_out = csv_out.slice(0, -1) // Remove the last ","
csv_out += "\n"

for (var i = 0; i < data[Object.keys(data)[0]].length; i++) {
	for (const key of Object.keys(data)) {
		csv_out += data[key][i] + ","
	}
	csv_out = csv_out.slice(0, -1) // Remove the last ","
	csv_out += "\n"
}

save("selected.csv", csv_out)
