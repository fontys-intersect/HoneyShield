function myFunction() {
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    //table = document.getElementById('myTable');
    table = document.getElementsByClassName('table-hover')[0];
    tr = table.getElementsByTagName('tr');
    for (i = 0; i < tr.length; i++) {
        if (i == 0) continue; // skip first row (header)
        var displayRow = false;
        for (j = 0; j < tr[i].cells.length; j++) {
            td = tr[i].cells[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                displayRow = true;
                break;
                }
            }
        }
            tr[i].style.display = displayRow ? '' : 'none';
        }
}
