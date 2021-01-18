{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    var user_choice ="{{ user_choice }}";
    console.log("user_choice="+user_choice);
    console.log("base url="+base_url);
  </script>
  <script src="{{ base_url }}/grader/static/js/exportGrades.js"></script>

{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/export_grades"></a>Export Grades/<a href="{{ base_url }}/grader/export_grades/export_common"></a>Export</li>
{%- endblock -%}
{%- block body -%}
  <div id="table"></div>
  <div class="option" id="options">
    <div class='icon'><i class="fa fa-download" aria-hidden="true"></i></div>
    <div class='label' id="download">
    </div>
  </div>
{%- endblock -%}