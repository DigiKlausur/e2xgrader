$.ajax({
      url: base_url+"/formgrader/api/assignments",
      type: 'get',
      success: function (response) {
        console.log(response);
        console.log($.parseJSON(response));
        let assignments = $.parseJSON(response);
        let table = $('<table/>');
        table
          .addClass('e2xtable')
          .attr('id' , 'main_table')
          .append(
            $('<thead/>').append(
              $('<tr/>')
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        /*body.attr('id' , 'main_table');
        assignments.forEach(function (assignment) {
          body.append(
            $('<tr/>')
              .append($('<td/>').append($('<a/>').attr('href', '{{ base_url }}/grader/assignment/' + assignment['name']).text(assignment['name'])))
              .append($('<td/>').text(assignment['duedate']))
              .append($('<td/>').text(assignment['status']))
              .append($('<td/>').text(assignment['num_submissions']))
          );
        });*/

        $('#table').append(table.append(body));
        table.DataTable({
        ajax: '{{base_url}}/formgrader/api/assignments',
        order: [[1, 'asc']],
        columnDefs:[
            {
                targets: 0,
                searchable: false,
                orderable: true,
                render: function(data){
                   data = '<input type="radio" name="id" value="' + data + '">';
                   return data;
                }
            }
        ]
      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the assignment infos');
      }
    });