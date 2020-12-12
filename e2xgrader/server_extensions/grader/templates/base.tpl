<!DOCTYPE html>
<head>
    {%- block title -%}
    {%- endblock -%}
    <title>e2xgrader</title>
    {%- block head -%}
    <script src="{{ base_url }}/grader/static/components/jquery/jquery.min.js"></script>
    <script src="{{ base_url }}/grader/static/components/jquery/jquery.js"></script>
    <script src="{{ base_url }}/grader/static/components/fontawesome/js/all.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/datatables.net/js/jquery.dataTables.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/datatables.net-bs/js/dataTables.bootstrap.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/bootstrap/js/bootstrap.min.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/underscore/underscore.js"></script>
    <script src="{{ base_url }}/formgrader/static/components/backbone/backbone.js"></script>
    <script src="{{ base_url }}/formgrader/static/js/backbone_xsrf.js"></script>
    <script src="{{ base_url }}/static/components/requirejs/require.js"></script>
    <script type="text/javascript">
        require.config({
            baseUrl: 'static',
            paths: {
                jquery: 'components/jquery/jquery.min'
            }
        })
        var base_url = "{{ base_url }}";
    </script>
    <script src="{{ base_url }}/formgrader/static/js/utils.js"></script>
    <script src="{{ base_url }}/grader/static/js/manage_assignments.js"></script>
    <script src="{{ base_url }}/formgrader/static/js/manage_students.js"></script>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.22/css/jquery.dataTables.min.css" />
    <link rel="stylesheet" href="https://cdn.datatables.net/select/1.3.1/css/select.dataTables.min.css" />
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/bootstrap/css/bootstrap.min.css" />
    <link rel="stylesheet" href="{{ base_url }}/formgrader/static/components/datatables.net-bs/css/dataTables.bootstrap.min.css">
    <link rel="stylesheet" href="{{ base_url }}/grader/static/css/grader.css" type="text/css">
    {%- endblock -%}
</head>
<body>
    <div id="page">
        <div id="header">
            <div id="home" onclick="window.location='{{ base_url }}/grader'"><h1>e²xgrader</h1></div>
            {%- block pagetitle -%}

            {%- endblock -%}
            <div id="breadcrumbs">
                
                <ul>
                    {%- block breadcrumbs -%}
                    <li><a href="{{ base_url }}/grader/"><i class='fa fa-home'></i></a></li>
                    {%- endblock -%}
                </ul>
                
            </div>
        </div>
        <div id="body">
            {%- block body -%}
            {%- endblock -%}
        </div>
    </div>
</body>
</html>