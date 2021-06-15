{%- extends 'nbassignment/base.tpl' -%}

{% block head %}
<script type="text/javascript">
    let pool = '{{ pool }}';
</script>
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/tasks.js'></script>

{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#task-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Tasks</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/taskcreator/pools">Task Pools</a></li>
    <li>> {{ pool }}</li>
</ul>
</div>

<div class='help'>
<h3>Tasks</h3>
<p>Dummy help.</p>
</div>


<div class='test'>
    <table class='e2xtable'>
        <thead>
            <th>Name</th>
            <th># of Questions</th>
            <th>Points</th>
            <th>Edit</th>
            <th>Remove</th>
        </thead>
        <tbody id='task_table'>
            <tr><td>Loading...</td><td></td><td></td><td></td><td></td></tr>
        </tbody>
    </table>
</div>

{% endblock body %}