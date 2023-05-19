{%- extends 'authoring/tablebase.tpl' -%}

{% block head %}
{{ super() }}
<script src='{{ base_url }}/e2x/authoring/static/js/templates.js'></script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#template-link').addClass("active");
</script>
{% endblock sidebar %}


{% block headline %}
<h1>Templates</h1>
{% endblock headline %}
{% block breadcrumbs %}
<li><a href="{{ base_url }}/e2x/authoring/app/templates">Templates</a></li>
{% endblock breadcrumbs %}

{% block help %}
<h3>Create and edit templates</h3>
<p>Templates are used for creating exercises. A template consists of header and footer cells and special cells like student info.
You can use variables in templates by enclosing them in double curly braces (e.g. <strong>{{ my_var }}</strong>. 
When creating an exercise you can set the values for those variables.</p>
{% endblock help %}


{% block table_head %}
<th>Name</th>
<th>Edit</th>
<th>Remove</th>
{% endblock table_head %}
{% block table_body %}
<tr><td>Loading...</td><td></td><td></td></tr>
{% endblock table_body %}
{% block add_new %}
<button onclick="newTemplate()" id="add-template" class="btn btn-primary">Add Template</button>
{% endblock add_new %}
