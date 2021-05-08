function generateAssignment(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id,
            type: 'post',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return
}

function releaseAssignment(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id+"/release",
            type: 'post',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return
}

function collectAssignment(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id+"/collect",
            type: 'post',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return
}

function generateFeedbackAll(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id+"/generate_feedback",
            type: 'post',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return

}

function releaseFeedbackAll(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id+"/release_feedback",
            type: 'post',
            success: function (response) {
                var result = $.parseJSON(response);
                console.log(result);
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return

}