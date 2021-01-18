
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
        console.log(selection)
        return format();
    } else {
        selection = _.without(selection, obj.id);
        return;
    }

}

function onSelectall (obj) {
    //obj = Object type DOM element
    // Get the checkbox and see state, put value to array respective to state
    if(obj.checked === true){
       let checkboxes = document.getElementsByName("checkbox");
       checkboxes.forEach(function (checkbox){
            checkbox.checked = true;
            selection.push(checkbox.id);
            console.log(selection);
       });
    } else {
        document.getElementsByName("checkbox").forEach(function (checkbox){
            checkbox.checked = false;
            selection.push(checkbox.id);
            console.log(selection);
        });
        selection = [];
    }
    return;
}

function recieveData (){
    $.ajax({
      url: base_url+"/formgrader/api/assignments",
      type: 'put',
      data: selection,
      success: function (response) {
        console.log("suppossed to get selected data as csv");
      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the assignment infos');
      }
    });
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