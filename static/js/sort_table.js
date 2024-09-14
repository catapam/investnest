// Function to sort the table based on the column index
function sortTable(columnIndex) {
    var table = document.getElementById("asset-table");
    var tbody = table.getElementsByTagName("tbody")[1]; // Ensure you are targeting the second tbody with data
    var rows = Array.from(tbody.getElementsByTagName("tr")); // Convert rows to an array for sorting
    var switching = true;
    var direction = "asc"; // Default sort direction
    var switchCount = 0;

    while (switching) {
        switching = false;

        for (var i = 0; i < rows.length - 1; i++) {
            var shouldSwitch = false;
            var x = rows[i].getElementsByTagName("td")[columnIndex];
            var y = rows[i + 1].getElementsByTagName("td")[columnIndex];

            // Compare based on direction
            if (direction === "asc") {
                if (isNaN(x.innerHTML) && x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                } else if (!isNaN(x.innerHTML) && parseFloat(x.innerHTML) > parseFloat(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            } else if (direction === "desc") {
                if (isNaN(x.innerHTML) && x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                } else if (!isNaN(x.innerHTML) && parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchCount++;
        } else {
            if (switchCount === 0 && direction === "asc") {
                direction = "desc";
                switching = true;
            }
        }
    }
}
