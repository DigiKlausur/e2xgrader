{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    var assignment_id = "{{ assignment_id }}";
  </script>
  <script src="{{ base_url }}/grader/static/js/assignmentCommon.js"></script>
{%- endblock -%}

{%- block breadcrumbs -%}
  {{super()}}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}

{%- block body -%}
  <div id="table">
  <table id="datatableAssignment" class="display " style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Number of Submissions</th>
            </tr>
        </thead>
  </table>
  </div>
  <div class="option" id="grading" >
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading</h3>
    </div>
  </div>
  <div class="option" id="exchange" >
    <div class='icon'><i class='fa fa-exchange-alt'></i></div>
    <div class='label'>
      <h3>Exchange</h3>
    </div>
  </div>

{%- endblock -%}