{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url ="{{ base_url }}";
  </script>
  <script type="text/javascript" src="{{ base_url }}/grader/static/js/manage_assignments.js></script>

{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}
{%- block body -%}
  <div id="table"></div>
  <div class="option" id="options" onclick="createAssignmentModal();">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Add Assignment</h3>
    </div>
  </div>
{%- endblock -%}