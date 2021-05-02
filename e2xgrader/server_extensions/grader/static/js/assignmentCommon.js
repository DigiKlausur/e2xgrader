var notebookList = [];

$.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
        var result = $.parseJSON(response);
        console.log(typeof(result));
        console.log(result['name']);
        document.getElementById('name').innerHTML = result['name'];
        document.getElementById('duedate').innerHTML = result['duedate'];
        document.getElementById('status').innerHTML = result['status'];
        document.getElementById('num_submissions').innerHTML = result['num_submissions'];
        $.ajax({
            url: base_url+"/formgrader/api/notebooks/"+assignment_id,
            type: 'get',
            success: function (response) {
                var result = $.parseJSON(response);

                $(document).ready(function() {
                    var table = $('#notebookList').DataTable({
                        "data": result,
                        "columns": [
                            {
                              "orderable": false,
                              "data": "name",
                              "render": function (name) {
                                    return '<input type="checkbox" id="'+assignment_id+'/'+name+'" name="checkbox" onclick="submitNotebook(this)">';
                              }
                            },
                            { "data": "name"},
                            { "data": "needs_manual_grade" },
                            { "data": "num_submissions" }
                        ],
                        "order": [[1, 'asc']],
                        "bPaginate": false,
                        "bLengthChange": false,
                        "bFilter": true,
                        "bInfo": false,
                        "bAutoWidth": false
                    });
                });
            },
            error: function (xhr) {
                console.log('Something went wrong when fetching the information....contact administration');
            }
        });


      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });

function toggleView(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function submitNotebook(obj) {

    if(obj.checked === true){
        if(_.contains(notebookList, obj.id) === false){
            notebookList.push(obj.id);
        }
    } else {
        notebookList = _.without(notebookList, obj.id);
    }
    console.log(notebookList);
}