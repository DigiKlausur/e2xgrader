{%- extends 'base.tpl' -%}

{%- block title -%}
Manual Grading
{%- endblock -%}

{%- block sidebar -%}
    {{ super() }}
    <script type="text/javascript">
        $('#gradebook').addClass('active');
    </script>
{%- endblock -%}