{%- extends 'nbassignment/base.tpl' -%}

{% block head %}
<script type="text/javascript">
    let assignment = '{{ assignment }}';
    console.log(assignment);
</script>
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/exercises.js'></script>

{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#exercise-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Assignments</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/taskcreator/assignments">Assignments</a></li>
    <li> > {{ assignment }} </li>
</ul>
</div>

<div class='help'>
<h3>Choose your exercise</h3>
<p>Here you can choose or create an exercise. An exercise is a single Jupyter Notebook consisting of tasks..</p>
</div>


<div class='test'>
    <table class='e2xtable'>
        <thead>
            <th>Name</th>
            <th>Remove</th>
        </thead>
        <tbody id='exercise_table'>
            <tr><td>Loading...</td><td></td></tr>
        </tbody>
    </table>
</div>

{% endblock body %}