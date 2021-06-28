{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script>
    var base_url = "{{ base_url }}";
    var assignment_id = "{{ assignment_id }}";
    var course_dir = "{{ course_dir }}";
  </script>

{%- endblock -%}

{%- block breadcrumbs -%}
  {{super()}}
  <li>/ <a href="{{ base_url }}/grader/assignments">Assignments</a>/<a href="{{ base_url }}/grader/assignments/assignment_common/?assignment_id={{ assignment_id }}">Assignment details</a>
  /<a href="{{ base_url }}/grader/assignments/assignment_common/grading_common/?assignment_id={{ assignment_id }}">Grading</a></li>
{%- endblock -%}

{%- block body -%}
  <script src="{{ base_url }}/grader/static/js/gradingAutoGradingAssignment.js"></script>
  <div id="description">
        <h4 id='message_header'>Here you can find the assignment details.</h4>
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
        <h4>Here you can find the submission list linked to the mentioned assignment.</h4>
        <p>If the status is 'needs autograding' please autograde it first by clicking the <i class="fa fa-bolt"></i> icon</p>
  </div>
  <div id='notebookTable'>
        <table id="submissionList" class="display " style="width:90%">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Student Name</th>
                        <th>Timestamp</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Autograde</th>

                    </tr>
                </thead>
        </table>
  </div>
  </div>

{%- endblock -%}