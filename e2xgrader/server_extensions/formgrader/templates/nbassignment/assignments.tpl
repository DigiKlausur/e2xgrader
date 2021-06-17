{%- extends 'nbassignment/tablebase.tpl' -%}

{% block head %}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/assignments.js'></script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#exercise-link').addClass("active");
</script>
{% endblock sidebar %}

{% block headline %}
<h1>Assignments</h1>
{% endblock headline %}
{% block breadcrumbs %}
<li><a href="{{ base_url }}/taskcreator/assignments">Assignments</a></li>
{% endblock breadcrumbs %}

{% block help %}
<h3>Choose your assignment</h3>
<p>Here you can choose which assignment you want to create an exercise for. An exercise is a single Jupyter Notebook consisting of tasks. Assignments have to be created via <a href="{{ base_url }}/formgrader/" target="_blank">nbgrader</a>.</p>
{% endblock help %}

{% block table_head %}
<th>Name</th>
<th>Number of Exercises</th>
{% endblock table_head %}
{% block table_body %}
<tr><td>Loading...</td><td></td></tr>
{% endblock table_body %}
