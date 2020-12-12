
let selection = [];
let onSelect = function(id) {
  // Get the checkbox
  selection.push(id);
  console.log(selection);
  return;

}

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
          .append(
            $('<thead/>').append(
              $('<tr/>')
                .append($('<th/>').text(' '))
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        body.attr('id' , 'main_table');
        assignments.forEach(function (assignment) {
          console.log(assignment);
          body.append(
            $('<tr/>')
              .append($('<input />', {
                type : 'checkbox',
                value: 0,
                }).attr( 'onclick', "onSelect("+assignment['id']+")"))
              .append($('<td/>').append($('<a/>').attr('href', base_url+'/grader/assignment/' + assignment['name']).text(assignment['name'])))
              .append($('<td/>').text(assignment['duedate']))
              .append($('<td/>').text(assignment['status']))
              .append($('<td/>').text(assignment['num_submissions']))
          );
        });

        $('#table').append(table.append(body));
      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the assignment infos');
      }
    });