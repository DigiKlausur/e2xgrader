{%- extends 'task_view/gradebook_base.tpl' -%}

{%- block head -%}
<script>
var assignment_id = "{{ assignment_id }}";
var notebook_id = "{{ notebook_id }}";
var task_id = "/{{ task_id }}";
var view = "task";
</script>

<script src="{{ base_url }}/e2xgrader/static/js/gradebook_notebook_submissions.js"></script>
{%- endblock head -%}

{%- block breadcrumbs -%}
<ol class="breadcrumb">
  <li><a href="{{ base_url }}/formgrader/gradebook/?view=task">Manual Grading (Task View)</a></li>
  <li><a href="{{ base_url }}/formgrader/gradebook/{{ assignment_id }}/?view=task">{{ assignment_id }}</a></li>
  <li><a href="{{ base_url }}/formgrader/gradebook/tasks/{{ assignment_id }}/{{ notebook_id }}">{{ notebook_id }}</a></li>
  <li class="active">{{ task_id }}</li>
</ol>
{%- endblock -%}

{%- block table_header -%}
<tr>
  <th></th>
  <th>Submission ID</th>
  <th class="text-center">Overall Score</th>
  <th class="text-center">Code Score</th>
  <th class="text-center">Written Score</th>
  <th class="text-center">Task Score</th>
  <th class="text-center">Needs Manual Grade?</th>
  <th class="text-center">Tests Failed?</th>
  <th class="text-center">Flagged?</th>
</tr>
{%- endblock -%}

{%- block table_body -%}
<tr><td colspan="8">Loading, please wait...</td></tr>
{%- endblock -%}
