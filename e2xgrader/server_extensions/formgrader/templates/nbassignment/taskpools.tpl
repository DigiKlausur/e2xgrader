{%- extends 'nbassignment/tablebase.tpl' -%}

{% block head %}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/taskpools.js'></script>

{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#task-link').addClass("active");
</script>
{% endblock sidebar %}

{% block headline %}
<h1>Task Pools</h1>
{% endblock headline %}
{% block breadcrumbs %}
<li><a href="{{ base_url }}/taskcreator/pools">Task Pools</a></li>
{% endblock breadcrumbs %}

{% block help %}
<h3>Manage task pools</h3>
<p>Task pools are collections of tasks about the same topic. A task consists of a collection of related questions.</p>
{% endblock help %}

{% block table_head %}
<th>Name</th>
<th>Number of Tasks</th>
<th>Remove</th>
{% endblock table_head %}
{% block table_body %}
<tr><td>Loading...</td><td></td><td></td><td></td></tr>
{% endblock table_body %}
{% block add_new %}
<button onclick="newPool()" class="btn btn-primary">Add Task Pool</button>
{% endblock add_new %}
