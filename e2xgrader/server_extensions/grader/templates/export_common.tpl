{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script src="{{ base_url }}/grader/static/js/exportGrades.js"></script>


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