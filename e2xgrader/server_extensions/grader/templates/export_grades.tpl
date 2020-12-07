{%- extends 'base.tpl' -%}

{%- block head -%}
{{ super() }}
<style type="text/css">
    #download_assignments svg {
  color: #008ffb;
}

#download_notebooks svg {
  color: #ef474a;
}

#download_tasks svg {
  color: #fdc006;
}
</style>
{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/export_grades/">Export Grades</a></li>
{%- endblock -%}

{%- block body -%}
<div id="description">
<h4>Here you can export grades</h4>
<p>You can either export the grades on an assignment level (total score per assignment per student) or on a notebook level (total score per notebook per student) or on a task level (total score per task per student).</p>
</div>
<!--<a target="_blank" href="{{ base_url }}/formgrader/export_grades/assignments" download="grades.csv">-->
<div class="option" id="download_assignments" onclick="window.location='{{ base_url }}/grader/export_common'">
    
    <div class='icon'><i class='fa fa-file-download'></i></div>
    <div class='label'>
      <h3>Assignments</h3>
      <p>Creates a table with one column per assignment</p>
    </div>
  </div>
</a>

<a target="_blank" href="{{ base_url }}/formgrader/export_grades/notebooks" download="grades.csv">
<div class="option" id="download_notebooks">
    
    <div class='icon'><i class='fa fa-file-download'></i></div>
    <div class='label'>
      <h3>Notebooks</h3>
      <p>Creates a table with one column per notebook per assignment</p>
    </div>
  </div>
</a>
<a target="_blank" href="{{ base_url }}/formgrader/export_grades/tasks" download="grades.csv">
<div class="option" id="download_tasks">
    
    <div class='icon'><i class='fa fa-file-download'></i></div>
    <div class='label'>
      <h3>Tasks</h3>
      <p>Creates a table with one column per task per notebook per assignment</p>
    </div>
  </div>
</a>

{%- endblock -%}