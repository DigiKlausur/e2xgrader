{%- extends 'task_view/gradebook_base.tpl' -%}

{%- block head -%}
<script>
var assignment_id = "{{ assignment_id }}";
var view = "task";
</script>

<script src="{{ base_url }}/e2xgrader/static/js/gradebook_notebooks.js"></script>
{%- endblock head -%}

{%- block breadcrumbs -%}
<ol class="breadcrumb">
  <li><a href="{{ base_url }}/formgrader/gradebook/?view=task">Manual Grading (Task View)</a></li>
  <li class="active">{{ assignment_id }}</li>
</ol>
{%- endblock -%}

{%- block table_header -%}
<tr>
  <th>Notebook ID</th>
  <th class="text-center">Avg. Score</th>
  <th class="text-center">Avg. Code Score</th>
  <th class="text-center">Avg. Written Score</th>
  <th class="text-center">Avg. Task Score</th>
  <th class="text-center">Needs Manual Grade?</th>
</tr>
{%- endblock -%}

{%- block table_body -%}
<tr><td colspan="6">Loading, please wait...</td></tr>
{%- endblock -%}
