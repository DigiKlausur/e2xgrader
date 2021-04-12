
let selection = [];

function getNotebooks(assignment_id){

    var notebook_list = "";
    $.ajax({
      url: base_url+"/formgrader/api/notebooks/"+assignment_id,
      type: 'get',
      async: false,
      success: function (response) {
            var notebooks = $.parseJSON(response);
            if (notebooks.length === 0)
            {
                notebook_list  = "<tr><td> No notebook to show</td></tr>";
            } else
            {
                notebooks.forEach(function (notebook) {
                    notebook_list += '<tr><td><input type="checkbox" id="'+assignment_id+'/'+notebook['name']+'" name="'+assignment_id+'checkbox" onclick="onSelect(this)"></td>'+
                            '<td>Notebook:</td>'+
                            '<td>'+notebook['name']+'</td>'+
                            '<td>Submissions:</td>'+
                            '<td>'+notebook['num_submissions']+'</td>'+
                    '</tr>';
                });
            }
      },
      error: function (error){
            notebook_list += '<tr><td>Error : '+error+'</td></tr>';
      }
    });
    return notebook_list;
}

function onSelect (obj) {
    //obj = Object type DOM element
    // Get the checkbox and see state, put value to array respective to state
    console.log("entered onSelect obj id="+obj.id);
    if(obj.checked === true){
        console.log("checked true");
        if(_.contains(selection, obj.id) === false){
            selection.push(obj.id);
            console.log("obj id:"+obj.id+" pushed getting child")

        }
    } else {
        selection = _.without(selection, obj.id);
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
            if(_.contains(selection, checkbox.id) === false)
                selection.push(checkbox.id);
                /*console.log(selection);
                checkbox.click();*/
       });
       console.log(selection);
    } else {
        document.getElementsByName("checkbox").forEach(function (checkbox){
            checkbox.checked = false;
        });
        selection = [];
    }
    console.log(selection);
    return;
}

function assignmentView ()  {
    $.ajax({
      url: base_url+"/formgrader/api/assignments",
      type: 'get',
      success: function (response) {
        var assignments = $.parseJSON(response);
        $(document).ready(function()
        {
           var table = $('#datatable_export').DataTable({
             "data": assignments,
             "columns": [
                 /*{
                     "className": 'details-control',
                     "orderable": false,
                     "data": "name",
                     "render": function (name) {
                         return '<input type="checkbox" id="'+name+'" name="checkbox" >';
                     },*/
                    {
                        'targets': 0,
                        'checkboxes': {
                            'selectRow': true
                        }
                    }
                 },
                 { "data": "name" },
                 { "data": "duedate" },
                 { "data": "status" },
                 { "data": "num_submissions" }
             ],
             'select': {
                'style': 'multi'
             },
             "order": [[1, 'asc']]
           });

           // Event listener for opening and closing details
           $('#datatable_export tbody').on('click', 'td.details-control', function ()
           {
                var tr = $(this).closest('tr');
                console.log(this.firstChild.id);
                var assignment_id = tr.find("td:eq(1)").text();
                var row = table.row(tr);
                var notebook_list = getNotebooks(assignment_id);
                if (row.child.isShown())
                {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else
                {
                    // Open this row
                    row.child(notebook_list).show();
                    tr.addClass('shown');
                    console.log("selection:"+selection);
                    if($(this).children("input").checked === true)
                    {
                        console.log("checked true");
                        if(_.contains(selection, $(this).children("input").id) === false)
                        {
                            selection.push(obj.id);
                            console.log(selection);
                            console.log("obj id:"+obj.id+" pushed getting child")
                            let checkboxes = document.getElementsByName($(this).children("input").id+"checkbox");
                            console.log("children:"+checkboxes);
                            checkboxes.forEach(function (checkbox)
                            {
                                checkbox.checked = true;
                                onSelect(checkbox);
                                console.log("checkbox click performed");
                            });

                        }
                    } else
                    {
                        selection = _.without(selection, $(this).children("input").id);
                    }
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

function downloadSelection(){
    // ajaX call to handler
    return;
}
assignmentView();