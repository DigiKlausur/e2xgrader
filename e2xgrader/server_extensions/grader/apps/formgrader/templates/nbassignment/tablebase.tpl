{%- extends 'nbassignment/base.tpl' -%}

{% block body %}

{% block headline %}
{% endblock %}
<div class='breadcrumbs'>
    <ul>
    {% block breadcrumbs %}
    {% endblock %}
    </ul>
</div>

<div class='help'>
    {% block help %}
    {% endblock %}
</div>


<div class='tablediv'>
    <table class='e2xtable'>
        <thead>
            {% block table_head %}
            {% endblock %}
        </thead>
        <tbody id='main_table'>
            {% block table_body %}
            {% endblock %}
        </tbody>
    </table>
    {% block add_new %}
    {% endblock %}
</div>

{% endblock body %}