<!doctype html>
<head>
    {%- block title -%}
    {%- endblock -%}
    <title>e2xgrader</title>
    {%- block head -%}
    <script src="{{ base_url }}/formgrader/static/components/jquery/jquery.min.js"></script>
    <script src="{{ base_url }}/grader/static/components/fontawesome/js/all.min.js"></script>
    <script src="{{ base_url }}/grader/static/components/underscore/underscore.js"></script>
    <script src="{{ base_url }}/grader/static/components/underscore/backbone.js"></script>
    <script src="{{ base_url }}/static/components/requirejs/require.js"></script>
    <script type="text/javascript">
        require.config({
            baseUrl: 'static',
            paths: {
                jquery: 'components/jquery/jquery.min'
            }
        })
    </script>
    <script src="{{ base_url }}/grader/static/js/manage_assignments.js"></script>
    <link rel="stylesheet" href="{{ base_url }}/grader/static/css/grader.css" type="text/css">
    {%- endblock -%}
</head>
<body>
    <div id="page">
        <div id="header">
            <h1>e²xgrader</h1>
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