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
            url: base_url+"/formgrader/api/submissions/"+assignment_id,
            type: 'get',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
                $(document).ready(function() {

                    var table = $('#submissionList').DataTable({
                        "data": result,
                        "columns": [
                            { "data": "student"},
                            { "data": "last_name",
                              "defaultContent": "<i>NA</i>",
                              "render":function(data,type,row,meta){
                                    var name = '';
                                    if(row['first_name'] === null && row['last_name'] === null)
                                        name = "NA,NA";
                                    else
                                        name = row['first_name']+','+row['last_name'];

                                    return name;

                              }
                            },
                            { "data": "timestamp",
                              "className": "dt-center",
                              "defaultContent": "<i>NA</i>"},
                            { "data": "needs_manual_grade",
                              "render": function(data,type,row,meta)
                              {
                                   if( row['needs_manual_grade'] ){
                                        return '<div class="label label-info">needs manual grading</div>'
                                    }
                                    else if( !row['autograded'] ){
                                        return '<div class="label label-warning">needs autograding</div>'
                                    }
                                    else
                                    {
                                        return '<div class="label label-success">graded</div>'
                                    }
                              }
                            },
                            { "data": "score",
                              "className": "dt-center"},
                            { "data": "autograded",
                              "className": "dt-center",
                              "render": function(status){
                                    if( !status ){
                                        return '<i class="fa fa-bolt"></i>'
                                    }
                                    return ''
                              }
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