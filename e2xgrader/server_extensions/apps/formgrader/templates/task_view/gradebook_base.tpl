{%- extends 'base.tpl' -%}

{%- block title -%}
Manual Grading (Task View)
{%- endblock -%}

{%- block sidebar -%}
    {{ super() }}
    <script type="text/javascript">
        $('#gradebook_questions').addClass('active');
    </script>
{%- endblock -%}