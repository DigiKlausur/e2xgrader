
let selection = [];
function getNotebooks (assignment_id) {
    $.ajax({
      url: base_url+"/formgrader/api/notebooks/srhb",
      type: 'get',
      success: function (response) {
        notebooks = $.parseJSON(response)
        $(document).ready(function() {
           table = $("#"+assignment_id).DataTable({
             "data": notebooks,
             "columns": [
                 {
                     "className": 'details-control',
                     "orderable": false,
                     "data": null,
                     "render": function () {
                         return '<input type="checkbox" name="checkbox">';
                     },
                 },
                 { "data": "name" },
                 { "data": "average_score" },
                 { "data": "num_submissions" }
             ],
             "order": [[1, 'asc']]
           });

           // Event listener for opening and closing details
           $("#"+assignment_id).on('click', 'td.details-control', function () {
                var tr = $(this).closest('tr');
                var notebook_id = tr.find("td:eq(1)").text();
                var row = table.row(tr);

                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    // Open this row
                    row.child( format( notebook_id ) ).show();
                    tr.addClass('shown');
                }
           });

        });
        return table;
      },
      error: function (error){
        let table = $('<table/>');
        table
          .addClass('e2xtable')
          .append(
            $('<thead align="center"/>').append(
              $('<tr/>')
                .append($('<th/>').text('Error'))
        ));
        let body = $('<tbody/>');
        body.attr('align', 'center');
        body.append($('<td/>').text("Something went wrong when fetching the information....contact administration"));
        $('#'+assignment_id).append(table.append(body));
        console.log('Something went wrong when fetching the information....contact administrator');
      }
    })
}

function format (id) {
    // returns table for collapsible
    return '<table id='+id+' cellpadding="5" cellspacing="0" border="0" style="padding-left:50px; width=100%">'+
        '<thead>'+
            '<tr>'+
                '<th><input type="checkbox" onclick="onSelectall(this)"></th>'+
                '<th>Name</th>'+
                '<th>Average Score</th>'+
                '<th>Number of Submissions</th>'+
            '</tr>'+
        '</thead>'+
        '</table>';
}

function onSelect (obj) {
    //obj = Object type DOM element
    // Get the checkbox and see state, put value to array respective to state
    var tr = obj.closest('tr');
    console.log(tr);
    /*
    var table = $('#datatable').DataTable();
    console.log(table);
    */
    var row = $('#datatable').row( tr );
    if(obj.checked === true){
        selection.push(obj.id);
        row.child( format() ).show();
        tr.addClass('shown');

    } else {
        selection = _.without(selection, obj.id);
        row.child.hide();
        tr.removeClass('shown');
    }
    console.log(selection);
    return;

}

function onSelectall (obj) {
    //obj = Object type DOM element
    // Get the checkbox and see state, put value to array respective to state
    if(obj.checked === true){
       let checkboxes = document.getElementsByName("checkbox");
       checkboxes.forEach(function (checkbox){
            checkbox.checked = true;
            selection.push(checkbox.id);
       });
    } else {
        document.getElementsByName("checkbox").forEach(function (checkbox){
            checkbox.checked = false;
        });
        selection = [];
    }
    console.log(selection);
    return;
}

function assignmentView () {
    $.ajax({
      url: base_url+"/formgrader/api/assignments",
      type: 'get',
      success: function (response) {
        var assignments = $.parseJSON(response);
        $(document).ready(function() {
           var table = $('#datatable').DataTable({
             "data": assignments,
             "columns": [
                 {
                     "className": 'details-control',
                     "orderable": false,
                     "data": null,
                     "render": function () {
                         return '<input type="checkbox" name="checkbox">';
                     },
                 },
                 { "data": "name" },
                 { "data": "duedate" },
                 { "data": "status" },
                 { "data": "num_submissions" }
             ],
             "order": [[1, 'asc']]
           });

           // Event listener for opening and closing details
           $('#datatable tbody').on('click', 'td.details-control', function () {
                var tr = $(this).closest('tr');
                var assignment_id = tr.find("td:eq(1)").text();
                var row = table.row(tr);

                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    // Open this row
                    row.child( '<table id='+assignment_id+' cellpadding="5" cellspacing="0" border="0" style="padding-left:50px; width=100%">'+'</table>' ).show();
                    tr.addClass('shown');
                    getNotebooks(assignment_id);
                }
           });
        });
        $('#download').html('<a target="_blank" href="{{ base_url }}/formgrader/export_grades/assignments" download="grades.csv"><h3>Download Selected Assignments</h3></a>');

      },
      error: function (xhr) {
        let table = $('<table/>');
        table
          .addClass('e2xtable')
          .append(
            $('<thead align="center"/>').append(
              $('<tr/>')
                .append($('<th/>').text('Error'))
        ));
        let body = $('<tbody/>');
        body.attr('align', 'center');
        body.append($('<td/>').text("Something went wrong when fetching the information....contact administration"));
        $('#table').empty();
        $('#table').append(table.append(body));
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });
}

function serveUserChoice (){
    if ( user_choice === "assignment" ){
        assignmentView();
    }

}

serveUserChoice();