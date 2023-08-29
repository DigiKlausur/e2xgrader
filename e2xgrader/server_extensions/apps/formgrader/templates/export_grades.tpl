{%- extends 'base.tpl' -%}

{%- block title -%}
Export Grades
{%- endblock -%}

{%- block sidebar -%}
    {{ super() }}
    <script type="text/javascript">
        $('#export_grades').addClass('active');
    </script>
{%- endblock -%}

{%- block table_body -%}

<h4>Here you can export grades</h4>
<p>You can either export the grades on an assignment level (total score per assignment per student) or on a notebook level (total score per notebook per student) or on a question level (total score per question per student).</p>
<form method="get" action="{{ base_url }}/formgrader/api/export_grades"/>
  <fieldset>
    <div>
      <legend>Level</legend>
      <input type="radio" name="level" id="assignment" value="assignment" />
      <label for="assignment">Show score per assignment</label><br />

      <input type="radio" name="level" id="notebook" value="notebook" checked />
      <label for="notebook">Show score per notebook</label><br />

      <input type="radio" name="level" id="task" value="task" />
      <label for="task">Show score per question</label><br />
    </div>
    <div>
      <legend>Advanced</legend>
      <input type="radio" name="normalize" id="no_normalization" value="false" checked />
      <label for="max_score">Do not add the maximum score</label><br />

      <input type="radio" name="normalize" id="max_score" value="max_score" />
      <label for="max_score">Add a row with the maximum score</label><br />

      <input type="radio" name="normalize" id="normalize" value="true" />
      <label for="max_score">Divide all scores by the maximum score</label><br />
    </div>
    <br />
    <input type="submit" value="Export Grades">
  </fieldset>
</form>
{%- endblock -%}