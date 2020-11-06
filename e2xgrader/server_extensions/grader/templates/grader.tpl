{%- extends 'base.tpl' -%}

{%- block head -%}
  {{super()}}

  <style type="text/css">
    #assignments svg {
      color: #008ffb;
    }

    #students svg {
      color: #ef474a;
    }

    #pools svg {
      color: #fdc006; 
    }

    #templates svg {
      color: #a2cf37;
    }

    #export svg {
      color: #995dea;
    }

  </style>    
{%- endblock -%}

{%- block body -%}
  <div class="option" id="assignments" onclick="window.location='{{ base_url }}/grader/assignments'">
    <div class='icon'><i class='fa fa-file-alt'></i></div>
    <div class='label'>
      <h3>Assignments</h3>
      <p>Create, grade, release and collect assignments</p>
    </div>
  </div>
  <div class="option" id="students" onclick="window.location='{{ base_url }}/grader/students'">
    <div class='icon'><i class='fa fa-user-friends'></i></div>
    <div class='label'>
      <h3>Students</h3>
      <p>Manage student information</p>
    </div>
  </div>
  <div class="option" id="export" onclick="window.location='{{ base_url }}/grader/export_grades'">
    <div class='icon'><i class='fa fa-download'></i></div>
    <div class='label'>
      <h3>Export</h3>
      <p>Export grades as csv files</p>
    </div>
  </div>
{%- endblock -%}