function addNewKey() {
	if(document.getElementById("new_key")==null) {
		table = document.getElementById("key_table");
		tbody = table.getElementsByTagName('tbody')[0];
		thead = table.getElementsByTagName('thead')[0];
		rowLen = thead.rows.length;
		newRow = tbody.insertRow(-1);

		newCel = newRow.insertCell(0);
		newCel.innerHTML = '<a href="javascript:submitNewKey()"><img src="/static/img/check.png" id="save"/></a>';

		newCel = newRow.insertCell(0);
		newCel.innerHTML = '<textarea id="new_key" name="new_key"></textarea>';

	}
}

function submitNewKey() {
	new_key = document.getElementById("new_key");
	if(new_key!=null) {
		new_key_value=new_key.value
		if(new_key_value!='') {
			document.getElementById("profile").submit();
		}
	}
}

function submitChangedKey() {
}

function editPubKey(key_id) {
	if(document.getElementById("new_key")==null) {
		table = document.getElementById("key_table");
		rows = table.getElementsByTagName("tr");
		for(i=0;i<rows.length;i++) {
			row = rows[i];
			cells = row.cells;
			for(j=0;j<cells.length;j++) {
				cell = cells[j];
				if(cell.className=='id') {
					if(cell.innerHTML==key_id) {
						cell.innerHTML = '<input type="hidden" name="key_id" value="'+key_id+'"/>'
						for(k=0;k<cells.length;k++) {
							edit_cell = cells[k];
							if(edit_cell.className=='key') {
								edit_cell.innerHTML = '<textarea id="new_key" name="update_key">'+edit_cell.innerHTML+'</textarea>';
							}
							if(edit_cell.className=='edit_link') {
								edit_cell.innerHTML = '<a title="Apply" href="javascript:submitNewKey()"><img src="/static/img/check.png" id="save"/></a>';
							}
							if(edit_cell.className=='delete_link') {
								edit_cell.innerHTML = '<a title="Cancel" href="javascript:location.reload()"><img src="/static/img/cancel.png" id="save"/></a>';
							}
						}
					}
				}
			}
		}
	}
}

function deletePubKey(key_id) {
	alert(key_id);
}
