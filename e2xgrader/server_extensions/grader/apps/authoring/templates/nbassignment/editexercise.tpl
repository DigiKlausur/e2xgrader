{%- extends 'nbassignment/base.tpl' -%}

{% block head %}
{{ super() }}
<link rel="stylesheet" href="{{ base_url }}/e2x/authoring/static/css/editexercise.css" type="text/css">
<script src="{{ base_url }}/e2x/authoring/static/js/makeexercise.js"></script>
{% endblock head %}

{% block sidebar %}
{{ super() }}
<script type="text/javascript">
    let assignment = "{{ assignment }}";
    $('#exercise-link').addClass("active");
</script>
{% endblock sidebar %}

{% block body %}

<h1>Edit Exercise - {{ exercise }}</h1>
<div class='breadcrumbs'>
<ul>
    <li><a href="{{ base_url }}/e2x/authoring/app/assignments">Assignments</a></li>
    <li> > <a href="{{ base_url }}/e2x/authoring/app/assignments/{{ assignment }}">{{ assignment }}</a></li>
    <li> > {{ exercise }}</li>
</ul>
</div>

<div>
    <div id="exercise">
        <h3>1. Please choose a name for your exercise</h3>
        <p class='help'>The name can contain upper and lower case letters. etc</p>
        <table class='e2xtable'>
            <tr>
                <td>Name</td><td><input type="text" id="exercise-name"></td>
            </tr>
        </table>
    </div>
    <div id="template" hidden>
        <h3>2. Please choose a template for your exercise</h3>
        <h4>2.1 Select the template</h4>
        <table class='e2xtable'>
            <tr>
                <td>Template</td><td><select id="template-select"><option value="">Choose a template</option></select></td>
            </tr>
        </table>
        <h4>2.2 Set variables of template</h4>
        <p>You can define variables in templates by enclosing them in curly braces (e.g.  <code>&#123;&#123; var &#125;&#125;</code> ). You can set the values here.</p>
        <table id='template-variables' class='e2xtable'>
            <thead><th>Variable</th><th>Value</th></thead>
            <tbody></tbody>
        </table>
    </div>
    <div id="tasks" hidden>
        <h3>3. Please select the tasks for your exercise</h3>
        <table class='e2xtable'>
            <tr>
                <td>Pool</td><td><select id="pool-select"><option value="">Choose a task pool</option></select></td>
            </tr>
        </table>
        <table class='e2xtable'>
            <thead>
                <tr><th>Selected Tasks</th><th>Controls</th><th>Available Tasks</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <select multiple="multiple" size="10" id='selected-tasks'></select>
                    </td>
                    <td>
                        <div id="task-controls">
                            <button class="btn btn-primary btn-controls" id="add">Add</button>
                            <button class="btn btn-primary btn-controls" id="remove">Remove</button>
                        </div>
                    </td>
                    <td>
                        <select multiple="multiple" size="10" id='available-tasks'></select>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div id="options" hidden>
        <h3>4. General options for the exercise</h3>
        <table id='exercise-options' class='e2xtable'>
            <thead><th>Option</th><th>Value</th></thead>
            <tbody>
                <tr><td>Add Task Headers</td><td><input type='checkbox' id='task-headers'></td></tr>
                <tr><td>Kernel</td><td><select id='kernel-select'></select></td></tr>
            </tbody>
        </table>
    </div>
</div>


{% endblock body %}