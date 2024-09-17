/**
 * Initializes the DataTable for the asset table once the document is fully loaded.
 * - Disables paging, info, and searching.
 * - Enables ordering for all columns except the first.
 */
$(document).ready(function() {
    // Initialize the DataTable for the element with ID 'asset-table'
    $('#asset-table').DataTable({
        "paging": false,       // Disable pagination, displaying all rows at once
        "ordering": true,      // Enable column-based ordering
        "info": false,         // Disable the table information display
        "searching": false,    // Disable the built-in search functionality
        "columnDefs": [
            { "orderable": false, "targets": 0 },    // Disable ordering for the first column (index 0)
            { "orderable": true, "targets": '_all' } // Enable ordering for all other columns
        ]
    });
});
