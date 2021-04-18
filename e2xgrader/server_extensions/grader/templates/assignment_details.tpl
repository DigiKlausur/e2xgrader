{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    var assignment_id = "{{ assignment_id }}";
    console.log("assig id:{{ assignment_id }}");
  </script>
  <script src="{{ base_url }}/grader/static/js/assignmentCommon.js"></script>
{%- endblock -%}

{%- block body -%}
  <div>
    assignment_id
  </div>

{%- endblock -%}