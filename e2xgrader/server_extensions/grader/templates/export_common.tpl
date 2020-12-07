{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
  </script>
  <script src="{{ base_url }}/grader/static/js/exportGrades.js"></script>

{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}
{%- block body -%}
  <div id="table"></div>
  <a target="_blank" href="{{ base_url }}/formgrader/export_grades/assignments" download="grades.csv">
  <div class="option" id="options">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Download Assignments</h3>
    </div>
  </div>
{%- endblock -%}