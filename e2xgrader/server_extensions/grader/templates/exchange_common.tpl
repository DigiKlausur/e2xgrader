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
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a>/<a href="{{ base_url }}/grader/assignments/assignment_common/?assignment_id={{ assignment_id }}">Assignment details</a></li>
{%- endblock -%}

{%- block body -%}
  <script src="{{ base_url }}/grader/static/js/assignmentCommon.js"></script>
  <script src="{{ base_url }}/grader/static/js/exchangeCommon.js"></script>
  <div id="description">
        <h4>Here you can find the assignment details.</h4>
        <p id='message'>Details of usage to be specified.</p>
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
  <div id='notebookTable'>
        <table id="notebookList" class="display " style="width:90%">
                <thead>
                    <tr>
                        <th>Notebook</th>
                        <th>Needs Manual Grading</th>
                        <th>Number of Submissions</th>
                    </tr>
                </thead>
        </table>
  </div>
  </div>

  <div class="option" id="generateAssignment" onclick='generateAssignment()'>
    <div class='icon'><i class='fas fa-plus'></i></div>
    <div class='label'>
      <h3>Generate Assignment</h3>
    </div>
  </div>
  <div class="option" id="releaseAssignment" onclick='releaseAssignment()'>
    <div class='icon'><i class='fas fa-file-export'></i></div>
    <div class='label'>
      <h3>Release Assignment</h3>
    </div>
  </div>
  <div class="option" id="collectAssignment" onclick='collectAssignment()'>
    <div class='icon'><i class='fas fa-file-import'></i></div>
    <div class='label'>
      <h3>Collect Assignment</h3>
    </div>
  </div>
  <div class="option" id="generateFeedback" onclick='generateFeedbackAll()'>
    <div class='icon'><i class='fas fa-head-side-virus'></i></div>
    <div class='label'>
      <h3>Generate Feedback</h3>
    </div>
  </div>
  <div class="option" id="releaseFeedback" onclick='releaseFeedbackAll()'>
    <div class='icon'><i class='fas fa-head-side-cough'></i></div>
    <div class='label'>
      <h3>Release Feedback</h3>
    </div>
  </div>

{%- endblock -%}