$.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
       var assignment = $.parseJSON(response);
       console.log(assignment);
        $(document).ready(function() {
           var table = $('#datatableAssignment').DataTable({
             "data": assignment,
             "columns": [
                 { "data": "name"},
                 { "data": "duedate" },
                 { "data": "status" },
                 { "data": "num_submissions" }
             ],
             "order": [[1, 'asc']]
           });
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