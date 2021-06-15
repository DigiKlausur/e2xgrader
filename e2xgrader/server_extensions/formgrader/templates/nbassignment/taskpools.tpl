{%- extends 'nbassignment/base.tpl' -%}

{% block head %}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/taskpools.js'></script>

{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#task-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Task Pools</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/taskcreator/pools">Task Pools</a></li>
</ul>
</div>

<div class='help'>
<h3>Manage task pools</h3>
<p>Task pools are collections of tasks about the same topic. A task consists of a collection of related questions.</p>
</div>


<div class='test'>
    <table class='e2xtable'>
        <thead>
            <th>Name</th>
            <th># of Tasks</th>
            <th>Edit</th>
            <th>Remove</th>
        </thead>
        <tbody id='pool_table'>
            <tr><td>Loading...</td><td></td><td></td><td></td></tr>
        </tbody>
    </table>
</div>

{% endblock body %}