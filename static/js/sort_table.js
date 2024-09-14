$(document).ready(function() {
    $('#asset-table').DataTable({
        "paging": false, 
        "ordering": true, 
        "info": false, 
        "searching": false, 
        "columnDefs": [
            { "orderable": false, "targets": 0 },
            { "orderable": true, "targets": '_all' }
        ]
    });
});