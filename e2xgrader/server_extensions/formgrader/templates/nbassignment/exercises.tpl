{%- extends 'nbassignment/tablebase.tpl' -%}

{% block head %}
<script type="text/javascript">
    let assignment = '{{ assignment }}';
</script>
{{ super() }}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/exercises.js'></script>
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
<li> > {{ assignment }} </li>
{% endblock breadcrumbs %}

{% block help %}
<h3>Choose your exercise</h3>
<p>Here you can choose or create an exercise. An exercise is a single Jupyter Notebook consisting of tasks..</p>
{% endblock help %}

{% block table_head %}
<th>Name</th>
<th>Remove</th>
{% endblock table_head %}
{% block table_body %}
<tr><td>Loading...</td><td></td></tr>
{% endblock table_body %}
{% block add_new %}
<button class="btn btn-primary">Add Exercise</button>
{% endblock add_new %}
