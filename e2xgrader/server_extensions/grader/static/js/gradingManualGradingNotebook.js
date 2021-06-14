function loadNotebooks(){
    $.ajax({
      url: base_url+"/formgrader/api/assignment/"+assignment_id,
      type: 'get',
      success: function (response) {
        var result = $.parseJSON(response);
        document.getElementById('assignmentName').innerHTML = result['name'];
        document.getElementById('notebookName').innerHTML = notebook_id;
        document.getElementById('duedate').innerHTML = result['duedate'];
        document.getElementById('status').innerHTML = result['status'];
        document.getElementById('num_submissions').innerHTML = result['num_submissions'];
        $.ajax({
            url: base_url+"/formgrader/api/submitted_notebooks/" + assignment_id + "/" + notebook_id,
            type: 'get',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
                $(document).ready(function() {
                    var table = $('#notebookSubmission').DataTable({
                        "data": result,
                        "columns": [
                            { "data": "id",
                              "render": function (name,type,row,meta) {
                                    var data = null;
                                    try {
                                        if (view === "task"){
                                            data = base_url+"/formgrader/submissions/" + name + "/?task=" + task_id;
                                        }
                                    }catch(err) {
                                        data = base_url+"/formgrader/submissions/" + name + "/?task=" + task_id;
                                    }
                                    //var data = base_url+"/formgrader/submissions/" + name;
                                    return '<a href='+data+'>Submission #'+row['index']+'</a>';
                                },
                            },
                            { "data": "score",
                              "render": function (name,type,row,meta) {
                                    return name+'/'+row['max_score'];
                                },
                            },
                            { "data": "score",
                              "render": function (name,type,row,meta) {
                                    return name+'/'+row['max_code_score'];
                                },
                            },
                            { "data": "written_score",
                              "render": function (name,type,row,meta) {
                                    return name+'/'+row['max_written_score'];
                                },
                            },
                            { "data": "task_score",
                              "render": function (name,type,row,meta) {
                                    return name+'/'+row['max_task_score'];
                                },
                            },
                            { "data": "needs_manual_grade",
                              "render": function (name,type,row,meta) {
                                    if(name)
                                        return '<i class="fas fa-check"></i>';
                                    else
                                        return '<i class="fas fa-check"></i>';
                                },
                            },
                            { "data": "failed_tests",
                              "render": function (name,type,row,meta) {
                                    if(name)
                                        return '<i class="fas fa-check"></i>';
                                    else
                                        return '<i class="fas fa-check"></i>';
                                },
                            },
                            { "data": "flagged",
                              "render": function (name,type,row,meta) {
                                    if(name)
                                        return '<i class="fas fa-check"></i>';
                                    else
                                        return '<i class="fas fa-check"></i>';
                                },
                            },
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