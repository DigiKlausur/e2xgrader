<!doctype html>
<head>
    <title>nbassignment</title>

    {%- block head -%}

    <script>
        let base_url = "{{ base_url }}";
        let url_prefix = "{{ url_prefix }}";
        let tree_url = base_url + '/tree/' + url_prefix + '/';
        let notebook_url = base_url + '/notebooks/' + url_prefix + '/';
    </script>
    <script src="{{ base_url }}/formgrader/static/components/jquery/jquery.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/underscore/underscore-min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/backbone/backbone-min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/bootstrap/js/bootstrap.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/datatables.net/js/jquery.dataTables.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/js/backbone_xsrf.js"></script>
    <script src="{{ base_url }}/formgrader/static/js/utils.js"></script>

    <script src='{{ base_url }}/e2x/authoring/static/js/base.js'></script>
    
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" href="{{ base_url }}/e2x/authoring/static/css/taskcreator.css" type="text/css">
    <link rel="stylesheet" href="{{ base_url }}/e2x/authoring/static/css/sidebar.css" type="text/css">
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/css/nbgrader.css">
    {%- endblock -%}    

</head>

<body>
    <div class="sidebar">
    {%- block sidebar -%}
    <h3>nbassignment</h3>
    <a href="{{ base_url }}/e2x/authoring/app/assignments" id="exercise-link">Manage Exercises</a>
    <a href="{{ base_url }}/e2x/authoring/app/pools" id="task-link">Manage Tasks</a>
    <a href="{{ base_url }}/e2x/authoring/app/templates" id="template-link">Manage Templates</a>
    {%- endblock -%}
    </div>
    <div class="body">
    {%- block body -%}
    {%- endblock -%}
    </div>
</body>