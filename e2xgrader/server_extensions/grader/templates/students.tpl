{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}
  <script type="text/javascript"src="{{ base_url }}/formgrader/static/js/manage_assignments.js"></script>
  <script type="text/javascript"src="{{ base_url }}/grader/static/js/manage_students.js"></script>


{%- endblock -%}

{%- block breadcrumbs -%}
  {{ super() }}
  <li>/ <a href="{{ base_url }}/grader/students">Students</a></li>
{%- endblock -%}

{%- block table_header -%}

         <tr>
         <th>Name</th>
         <th class="text-center">Student ID</th>
         <th class="text-center">Email</th>
         <th class="text-center">Overall Score</th>
         <th class="text-center no-sort">Edit Student</th>
         </tr>

{%- endblock -%}

{%- block button_holder -%}
  </div>
  <div class="option" id="options" onclick="createStudentModal();">
    <div class='icon'><i class='fa fa-plus'></i></div>
    <div class='label'>
      <h3>Add Student</h3>
    </div>
  </div>
{%- endblock -%}