{%- extends 'base.tpl' -%}

{% block head %}
<link rel="stylesheet" href="{{ base_url }}/taskcreator/static/css/editexercise.css" type="text/css">
<script type="module">    
    import {addTaskSelector, generateExercise, templateOptions, exerciseOptions} from "{{ base_url }}/taskcreator/static/js/editexercise.js";
    addTaskSelector({{ pools }}, "{{ base_url }}");
    templateOptions("{{ base_url }}");
    exerciseOptions("{{ base_url }}");
    generateExercise("{{ exercise }}", "{{ assignment }}", "{{ url_prefix }}", "{{ base_url }}");
</script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    $('#exercise-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Edit Exercise - {{ exercise }}</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/taskcreator/assignments">Assignments</a></li>
    <li> > <a href="{{ base_url }}/taskcreator/assignments/{{ assignment }}">{{ assignment }}</a></li>
    <li> > {{ exercise }}</li>
</ul>
</div>

<div>
    <div id="template-select">
        <h3>1. Template</h3>
        <label for="template">Choose a template:</label>
        <select name="template" id="template">
            <option value="">Choose a template</option>
            {% for template in templates %}
                <option value="{{ template.name }}">{{ template.name }}</option>
            {% endfor %}
        </select>
        <div id="template-options">
        </div>
    </div>
    <div id="task-select">
        <h3>2. Tasks</h3>
    </div>
    <div id="exercise-options">
        <h3>3. Exercise Options</h3>
    </div>
    <div id="generate">
        <h3>4. Generate Exercise</h3>
    </div>
</div>


{% endblock body %}