//console.log(view+" VIEW");
function loadNotebooks(){
    $.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
        var result = $.parseJSON(response);
        document.getElementById('assignment_name').innerHTML = result['name'];
        document.getElementById('notebook_name').innerHTML = notebook_id;
        document.getElementById('duedate').innerHTML = result['duedate'];
        document.getElementById('status').innerHTML = result['status'];
        document.getElementById('num_submissions').innerHTML = result['num_submissions'];
        $.ajax({
            url: base_url+"/formgrader/api/solution_cells/" + assignment_id + "/" + notebook_id,
            type: 'get',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
                $(document).ready(function() {
                    var table = $('#taskList').DataTable({
                        "data": result,
                        "columns": [
                            { "data": "name",
                              "render": function (name) {
                                    var data = base_url+"/grader/assignments/assignment_common/grading_common/manual_grading/notebook/" + assignment_id + "/" + notebook_id + "/?view=task&filter=" + name;
                                    return '<a href='+data+'>'+name+'</a>';
                                },
                            },
                            { "data": "avg_score",
                              "render": function (score,type,row,meta) {
                                     return score +'/'+row['max_score'];
                                }
                            },
                            { "data": "autograded"},
                            { "data": "needs_manual_grade"},

                        ],
                        "bPaginate": false,
                        "bLengthChange": false,
                        "bFilter": true,
                        "bInfo": false,
                        "bAutoWidth": false
                    });

                });
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

$(window).on('load', function () {
    loadNotebooks();
});