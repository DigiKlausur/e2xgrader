{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script type="text/javascript">
    $.ajax({
      url: "{{ base_url }}/formgrader/api/students",
      type: 'get',
      success: function (response) {
        console.log(response);
        console.log($.parseJSON(response));
        let students = $.parseJSON(response);
        let table = $('<table/>');
        table
          .addClass('e2xtable')
          .append(
            $('<thead/>').append(
              $('<tr/>')
                .append($('<th/>').text('Name'))
                .append($('<th/>').text('Student ID'))
                .append($('<th/>').text('Email'))
                .append($('<th/>').text('Overall Score'))
                .append($('<th/>').text('Edit'))
        ));
        let body = $('<tbody/>');
        body.attr('id' , 'main_table');
        students.forEach(function (student) {
          if (student['last_name'] == null) {
            student['last_name'] = 'None';
          }
          if (student['first_name'] == null) {
            student['first_name'] = 'None';
          }
          if (student['email'] == null) {
            student['email'] = 'None';
          }
          body.append(
            $('<tr/>')
              .append($('<td/>').text(student['last_name'] + ', ' + student['first_name']))
              .append($('<td/>').text(student['id']))
              .append($('<td/>').text(student['email']))
              .append($('<td/>').text(student['score'] + ' / ' + student['max_score']))
              .append($('<td/>').text('Edit'))
          );
        });

        $('#table').append(table.append(body));
      },
      error: function (xhr) {
        console.log('Something went wrong when fetching the student infos');
      }
    });
  </script>
  
{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/students">Students</a></li>
{%- endblock -%}
{%- block body -%}
  <div id="table"></div>
  <div class="option" id="options" onclick="createStudentModal();">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Add Student</h3>
    </div>
  </div>
{%- endblock -%}