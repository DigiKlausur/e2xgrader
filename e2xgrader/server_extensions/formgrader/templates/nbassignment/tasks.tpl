{%- extends 'nbassignment/tablebase.tpl' -%}

{% block head %}
<script type="text/javascript">
    let pool = '{{ pool }}';
</script>
{{ super() }}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/tasks.js'></script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#task-link').addClass("active");
</script>
{% endblock sidebar %}

{% block headline %}
<h1>Tasks</h1>
{% endblock headline %}
{% block breadcrumbs %}
<li><a href="{{ base_url }}/taskcreator/pools">Task Pools</a></li>
<li>> {{ pool }}</li>
{% endblock breadcrumbs %}

{% block help %}
<h3>Tasks</h3>
<p>Dummy help.</p>
{% endblock help %}

{% block table_head %}
<th>Name</th>
<th># of Questions</th>
<th>Points</th>
<th>Edit</th>
<th>Remove</th>
{% endblock table_head %}
{% block table_body %}
<tr><td>Loading...</td><td></td><td></td><td></td><td></td></tr>
{% endblock table_body %}
{% block add_new %}
<button onclick="newTask()" class="btn btn-primary">Add Task</button>
{% endblock add_new %}
