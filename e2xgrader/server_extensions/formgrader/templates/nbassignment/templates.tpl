{%- extends 'nbassignment/base.tpl' -%}

{% block head %}
<script src='{{ base_url }}/e2xgrader/static/js/nbassignment/templates.js'></script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#template-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Templates</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/taskcreator/templates">Templates</a></li>
</ul>
</div>

<div class='help'>
<h3>Create and edit templates</h3>
<p>Templates are used for creating exercises. A template consists of header and footer cells and special cells like student info.
You can use variables in templates by enclosing them in double curly braces (e.g. <strong>{{ my_var }}</strong>. 
When creating an exercise you can set the values for those variables.</p>
</div>


<div class='test'>
    <table class='e2xtable'>
        <thead>
            <th>Name</th>
            <th>Edit</th>
            <th>Remove</th>
        </thead>
        <tbody id='template_table'>
            <tr><td>Loading...</td><td></td><td></td></tr>
        </tbody>
    </table>
</div>

{% endblock body %}