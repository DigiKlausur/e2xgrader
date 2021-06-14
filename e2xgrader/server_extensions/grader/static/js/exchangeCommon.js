function generateAssignment(){
    // download handler call
    $.ajax({
            url: base_url+"/formgrader/api/assignment/"+assignment_id+"/assign",
            type: 'post',
            success: function (response) {
                response = $.parseJSON(response);
                if (response["success"]) {
                    createLogModal(
                        "success-modal",
                        "Success",
                        "Successfully created the student version of '" + assignment_id + "':",
                        response["log"]);

                } else {
                    createLogModal(
                        "error-modal",
                        "Error",
                        "There was an error creating the student version of '" + assignment_id + "':",
                        response["log"],
                        response["error"]);
                }
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
                response = $.parseJSON(response);
                if (response["success"]) {
                    createLogModal(
                        "success-modal",
                        "Success",
                        "Successfully released the student version of '" + assignment_id + "':",
                        response["log"]);

                } else {
                    createLogModal(
                        "error-modal",
                        "Error",
                        "There was an error releasing the student version of '" + assignment_id + "':",
                        response["log"],
                        response["error"]);
                }
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
                response = $.parseJSON(response);
                if (response["success"]) {
                    createLogModal(
                        "success-modal",
                        "Success",
                        "Successfully collected the student version of '" + assignment_id + "':",
                        response["log"]);

                } else {
                    createLogModal(
                        "error-modal",
                        "Error",
                        "There was an error collecting the student version of '" + assignment_id + "':",
                        response["log"],
                        response["error"]);
                }
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
                response = $.parseJSON(response);
                if (response["success"]) {
                    createLogModal(
                        "success-modal",
                        "Success",
                        "Successfully generated feedback of the student version of '" + assignment_id + "':",
                        response["log"]);

                } else {
                    createLogModal(
                        "error-modal",
                        "Error",
                        "There was an error in generating feedback of the student version of '" + assignment_id + "':",
                        response["log"],
                        response["error"]);
                }
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
                response = $.parseJSON(response);
                if (response["success"]) {
                    createLogModal(
                        "success-modal",
                        "Success",
                        "Successfully released feedback of the student version of '" + assignment_id + "':",
                        response["log"]);

                } else {
                    createLogModal(
                        "error-modal",
                        "Error",
                        "There was an error in releasing feedback of the student version of '" + assignment_id + "':",
                        response["log"],
                        response["error"]);
                }
            },
            error: function (xhr) {
                var result = $.parseJSON(xhr);
                console.log(result);
            }
        });
    return

}