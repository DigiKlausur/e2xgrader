
let selection = [];
function format () {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Full name:</td>'+
            '<td>example</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Extra info:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}

function onSelect (obj) {
    //obj = Object type DOM element
    // Get the checkbox and see state, put value to array respective to state
    if(obj.checked === true){
        selection.push(obj.id);
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

function assignmentView(){
    $.ajax({
      url: base_url+"/formgrader/api/assignments",
      type: 'get',
      success: function (response) {
        console.log(response);
        console.log($.parseJSON(response));
        var assignments = $.parseJSON(response);
        var table = $('<table/>');
        table
          .addClass('e2xtable')
          .append(
            $('<thead/>').append(
              $('<tr/>')
                .append($('<th/>').append($('<input />', {
                type : 'checkbox',
                id : 'all',
                value: 0,
                }).attr('onclick','onSelectall(this)')))
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        body.attr('id' , 'main_table');
        assignments.forEach(function (assignment) {
          body.append(
            $('<tr/>')
              .append($('<input />', {
                type : 'checkbox',
                id : assignment['id'],
                name: "checkbox",
                }).attr('onclick','onSelect(this)'))
              .append($('<td/>').append($('<a/>').attr('href', base_url+'/grader/assignment/' + assignment['name']).text(assignment['name'])))
              .append($('<td/>').text(assignment['duedate']))
              .append($('<td/>').text(assignment['status']))
              .append($('<td/>').text(assignment['num_submissions']))
          );
        });
        $('#table').append(table.append(body));
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
        $('#table').append(table.append(body));
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });
}

function taskView(){
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
                .append($('<th/>').append($('<input />', {
                type : 'checkbox',
                id : 'all',
                value: 0,
                }).attr('onclick','onSelectall(this)')))
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        body.attr('id' , 'main_table');
        assignments.forEach(function (assignment) {
          body.append(
            $('<tr/>')
              .append($('<input />', {
                type : 'checkbox',
                id : assignment['id'],
                name: "checkbox",
                }).attr('onclick','onSelect(this)'))
              .append($('<td/>').append($('<a/>').attr('href', base_url+'/grader/assignment/' + assignment['name']).text(assignment['name'])))
              .append($('<td/>').text(assignment['duedate']))
              .append($('<td/>').text(assignment['status']))
              .append($('<td/>').text(assignment['num_submissions']))
          );
        });

        $('#options').click(window.location='{{ base_url }}/grader/export_common');
        $('#options').attr("download", "grades.csv");
        $('#table').append(table.append(body));
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
        $('#table').append(table.append(body));
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });
}

function notebookView(){
    $.ajax({
      url: base_url + "/formgrader/api/assignments",
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
                .append($('<th/>').append($('<input />', {
                type : 'checkbox',
                id : 'all',
                value: 0,
                }).attr('onclick','onSelectall(this)')))
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        body.attr('id' , 'main_table');
        assignments.forEach(function (assignment) {
          body.append(
            $('<tr/>')
              .append($('<input />', {
                type : 'checkbox',
                id : assignment['id'],
                name: "checkbox",
                }).attr('onclick','onSelect(this)'))
              .append($('<td/>').append($('<a/>').attr('href', base_url+'/grader/assignment/' + assignment['name']).text(assignment['name'])))
              .append($('<td/>').text(assignment['duedate']))
              .append($('<td/>').text(assignment['status']))
              .append($('<td/>').text(assignment['num_submissions']))
          );
        });

        $('#options').click(window.location='{{ base_url }}/grader/export_common');
        $('#options').attr("download", "grades.csv");
        $('#table').append(table.append(body));
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
        $('#table').append(table.append(body));
        console.log('Something went wrong when fetching the information....contact administration');
      }
    });
}

function serveUserChoice (){
    if ( user_choice === "assignment" ){
        assignmentView();
    }
    else if ( user_choice === "notebook" ){
        notebookView();
    }
    else {
        taskView();
    }
}

serveUserChoice();