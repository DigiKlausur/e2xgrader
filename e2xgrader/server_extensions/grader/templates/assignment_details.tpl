{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script>
    var url_prefix = "{{ url_prefix }}";
    var base_url = "{{ base_url }}";
    var assignment_id = "{{ assignment_id }}";
  </script>

{%- endblock -%}

{%- block breadcrumbs -%}
  {{super()}}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a></li>
{%- endblock -%}

{%- block body -%}
  <script src="{{ base_url }}/grader/static/js/assignmentCommon.js"></script>
  <div id="description">
        <h4>Here you can find the assignment details.</h4>
        <p>Details of usage to be specified.</p>
  </div>
  <div id="table">
  <table style='border-collapse: collapse;width: 100%;'>
    <tr>
      <th style='padding: 8px;'>Assignment</th>
      <th style='padding: 8px;'>Duedate</th>
      <th style='padding: 8px;'>Status</th>
      <th style='padding: 8px;'>Number of Submissions</th>
    </tr>
    <tr>
      <td id='name' style='padding: 8px;'></td>
      <td id='duedate' style='padding: 8px;'></td>
      <td id='status' style='padding: 8px;'></td>
      <td id='num_submissions' style='padding: 8px;'></td>
    </tr>
  </table>
  <div id="notebookDescription">
        <h4>Here you can find the notebook list linked to the mentioned assignment.</h4>
        <p>Details of usage to be specified.</p>
  </div>
  <table id="notebookList" class="display " style="width:90%">
        <thead>
            <tr>
                <th></th>
                <th>Notebook</th>
                <th>Needs Manual Grading</th>
                <th>Number of Submissions</th>
            </tr>
        </thead>
  </table>
  </div>
  <div class="option" id="grading" onclick="toggleView('grading_buttons','exchange_buttons')">
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading</h3>
    </div>
  </div>
  <div class="option" id="exchange" onclick="toggleView('exchange_buttons','grading_buttons')">
    <div class='icon'><i class='fa fa-exchange-alt'></i></div>
    <div class='label'>
      <h3>Exchange</h3>
    </div>
  </div>

  <div id="grading_buttons" style="display:none;">
  <div class="optionButton" id="grading1" >
    <div class='icon'><i class='fa fa-address-card'></i></div>
    <div class='label'>
      <h3>Grading 1</h3>
    </div>
  </div>
  <div class="optionButton" id="grading2" >
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