{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    var assignment_id = "{{ assignment_id }}";
  </script>
  <script src="{{ base_url }}/grader/static/js/assignmentCommon.js"></script>
{%- endblock -%}

{%- block breadcrumbs -%}
  {{super()}}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}

{%- block body -%}
  <div id="table">
  <table id="datatableAssignment" class="display " style="width:100%">
        <thead>
            <tr>
                <th>Name</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Number of Submissions</th>
            </tr>
        </thead>
  </table>
  </div>
  <div class="option" id="grading" onclick="toggleView('grading_buttons')">
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading</h3>
    </div>
  </div>
  <div class="option" id="exchange" onclick="toggleView('exchange_buttons')">
    <div class='icon'><i class='fa fa-exchange-alt'></i></div>
    <div class='label'>
      <h3>Exchange</h3>
    </div>
  </div>

  <div id="grading_buttons" style="display:none;">
  <div class="option" id="grading1" >
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading 1</h3>
    </div>
  </div>
  <div class="option" id="grading2" >
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading 2</h3>
    </div>
  </div>
  </div>

  <div id="exchange_buttons" style="display:none;">
  <div class="option" id="exchange1" >
    <div class='icon'><i class='fa fa-exchange-alt'></i></div>
    <div class='label'>
      <h3>Exchange 1</h3>
    </div>
  </div>
  <div class="option" id="exchange2" >
    <div class='icon'><i class='fa fa-exchange-alt'></i></div>
    <div class='label'>
      <h3>Exchange 2</h3>
    </div>
  </div>
  </div>

{%- endblock -%}