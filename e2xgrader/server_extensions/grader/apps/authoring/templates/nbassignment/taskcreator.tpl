{%- extends 'base.tpl' -%}

{% block head %}
<script>
$(document).ready(function () {
    var table = $('<table/>')
        .attr('id', 'question_data')
        .addClass('e2xtable');
    var row = $('<tr/>');
    row.append($('<td/>').append('Name:'));
    row.append($('<td/>').append($('<input/>')
        .attr('type', 'text')
        .attr('id', 'qid')
    ));


    table.append(row);

    var link = $('<a/>').append('New Question').attr('href', '#');
    link.click( function () {
        if ($('#qid').val().trim() === '') {
            alert('You need to give a name!!!');

        } else {
            window.open("{{ base_url }}/e2x/authoring/app/new_question/" + $('#qid').val());
        }
    })
    var submit = $('<tr/>').append($('<td/>').attr('colspan', 2).append(link));
    table.append(submit);
    $('#create_question').append(table);//.append(link);


});
</script>
{% endblock head %}

{% block body %}

<h1> Hello </h1>

<div id="create_question">
</div>
{% endblock body %}