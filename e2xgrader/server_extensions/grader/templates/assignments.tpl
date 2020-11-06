{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script type="text/javascript">
    $.ajax({
      url: "{{ base_url }}/formgrader/api/assignments",
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
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Due Date'))
                .append($('<th/>').text('Status'))
                .append($('<th/>').text('# of Submissions'))
        ));
        let body = $('<tbody/>');
        assignments.forEach(function (assignment) {
          body.append(
            $('<tr/>')
              .append($('<td/>').append($('<a/>').attr('href', '{{ base_url }}/grader/assignment/' + assignment['name']).text(assignment['name'])))
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
  </script>
  
{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}
{%- block body -%}
  <div id="table"></div>
  <div class="option" id="options">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Add Assignment</h3>
    </div>
  </div>
{%- endblock -%}