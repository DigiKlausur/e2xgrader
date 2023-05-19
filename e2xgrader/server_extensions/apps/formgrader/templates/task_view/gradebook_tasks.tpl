{%- extends 'task_view/gradebook_base.tpl' -%}

{%- block head -%}
<script>
var assignment_id = "{{ assignment_id }}";
var notebook_id = "{{ notebook_id }}";
var view = "task";
</script>

<script src="{{ base_url }}/e2xgrader/static/js/gradebook_tasks.js"></script>
{%- endblock head -%}

{%- block breadcrumbs -%}
<ol class="breadcrumb">
  <li><a href="{{ base_url }}/formgrader/gradebook/?view=task">Manual Grading (TaskView)</a></li>
  <li><a href="{{ base_url }}/formgrader/gradebook/{{ assignment_id }}/?view=task">{{ assignment_id }}</a></li>
  <li class="active">{{ notebook_id }}</li>
</ol>
{%- endblock -%}

{%- block table_header -%}
<tr>
  <th>Task ID</th>
  <th class="text-center">Avg. Score</th>
  <th class="text-center">Is Autograded?</th>
  <th class="text-center">Needs Manual Grade?</th>
</tr>
{%- endblock -%}

{%- block table_body -%}
<tr><td colspan="5">Loading, please wait...</td></tr>
{%- endblock -%}
