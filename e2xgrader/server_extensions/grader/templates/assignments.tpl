{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    console.log(base_url);
  </script>
{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}
{%- block body -%}
  <div id="table">
  <table id="datatable" class="display " style="width:100%">
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
  <div class="option" id="options" onclick="createAssignmentModal();">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Add Assignment</h3>
    </div>
  </div>
{%- endblock -%}