{%- extends 'base.tpl' -%}

{%- block title -%}
Manage Students
{%- endblock -%}

{%- block sidebar -%}
    {{ super() }}
    <script type="text/javascript">
        $('#manage_students').addClass('active');
    </script>
{%- endblock -%}
