var totalNotebook = 0;

function loadNotebooks(){
    $.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
        var result = $.parseJSON(response);
        document.getElementById('name').innerHTML = result['name'];
        document.getElementById('duedate').innerHTML = result['duedate'];
        document.getElementById('status').innerHTML = result['status'];
        document.getElementById('num_submissions').innerHTML = result['num_submissions'];
        $.ajax({
            url: base_url+"/formgrader/api/notebooks/"+assignment_id,
            type: 'get',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
                $(document).ready(function() {
                    var table = $('#notebookList').DataTable({
                        "data": result,
                        "columns": [
                            { "data": "name"},
                            { "data": "needs_manual_grade"},
                            { "data": "num_submissions"}
                        ],
                        "bPaginate": false,
                        "bLengthChange": false,
                        "bFilter": true,
                        "bInfo": false,
                        "bAutoWidth": false
                    });
                });

                if( response === '[]'){
                    var grading = document.getElementById("grading");
                    var exchange = document.getElementById("exchange");
                    grading.style.display = "none";
                    exchange.style.display = "none";
                }
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
                $('#notebookTable').empty();
                $('#notebookTable').append(table.append(body));
                console.log('Something went wrong when fetching the information....contact administration');
            }
        });
        return true;

      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the information....contact administration');
        $('#table').empty();

        var exchange = document.getElementById('exchange');
        var grading = document.getElementById('grading');
        if (exchange !== null && grading !== null){
            exchange.style.display = 'none';
            grading.style.display = 'none';
        }

        document.getElementById('message').innerHTML = 'Something went wrong when fetching the information....contact administration';
        return false;
      }
    });
}

function toggleView(id1,id2) {
  var element1 = document.getElementById(id1);
  var element2 = document.getElementById(id2);
  if (element1.style.display === "none") {
    element1.style.display = "block";
    if(element2.style.display === "block"){
       element2.style.display = "none";
    }
  } else {
    element1.style.display = "none";
  }
}

$(window).on('load', function () {
    loadNotebooks();
});