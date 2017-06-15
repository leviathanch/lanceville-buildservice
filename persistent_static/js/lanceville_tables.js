function addNewKey() {
	table = document.getElementById("key_table");
	tbody = table.getElementsByTagName('tbody')[0];
	thead = table.getElementsByTagName('thead')[0];
	rowLen = thead.rows.length;
	newRow = tbody.insertRow(0);
	newCel = newRow.insertCell(0);
	newCel.innerHTML = "NEW CELL1";
	alert(newRow);
}
