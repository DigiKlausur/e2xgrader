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
  <div id="description">
        <h4>Here you can export grades</h4>
        <p>You can either export the grades on an assignment level (total score per assignment per student) or on a notebook level (total score per notebook per student) or on a task level (total score per task per student).</p>
  </div>
  <div id="table">
  <table id="datatable" class="display e2xtable" style="width:100%">
        <thead>
            <tr>
                <th><input type="checkbox" onclick="onSelectall(this)"></th>
                <th>Name</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Number of Submissions</th>
            </tr>
        </thead>
  </table>
  </div>
  <div class="option" id="options">
    <div class='icon'><i class="fa fa-download" aria-hidden="true"></i></div>
    <div class='label' id="download">
    </div>
  </div>
{%- endblock -%}