var Submission = Backbone.Model.extend({
    idAttribute: 'student',
    urlRoot: base_url + "/formgrader/api/submission/" + assignment_id
});

var Submissions = Backbone.Collection.extend({
    model: Submission,
    url: base_url + "/formgrader/api/submissions/" + assignment_id
});

var SubmissionUI = Backbone.View.extend({

    events: {},
 
    initialize: function () {
        this.$student_name = this.$el.find(".student-name");
        this.$student_id = this.$el.find(".student-id");
        this.$timestamp = this.$el.find(".timestamp");
        this.$status = this.$el.find(".status");
        this.$score = this.$el.find(".score");
        this.$autograde = this.$el.find(".autograde");
        this.$generate_feedback = this.$el.find(".generate-feedback");
        this.$release_feedback = this.$el.find(".release-feedback");
        this.$autograde_all = this.$el.find(".autograde-all");

        this.listenTo(this.model, "sync", this.render);
        this.render();
    },

    clear: function () {
        this.$student_name.empty();
        this.$student_id.empty();
        this.$timestamp.empty();
        this.$status.empty();
        this.$score.empty();
        this.$autograde.empty();
        this.$generate_feedback.empty();
        this.$release_feedback.empty();
        this.$autograde_all.empty();
    },

    render: function () {
        this.clear();

        var student = this.model.get("student");
        var assignment = this.model.get("name");

        // student name
        var last_name = this.model.get("last_name");
        var first_name = this.model.get("first_name");
        if (last_name === null) last_name = "None";
        if (first_name === null) first_name = "None";
        var name = last_name + ", " + first_name;
        this.$student_name.attr("data-order", name);
        if (this.model.get("autograded")) {
            this.$student_name.append($("<a/>")
                .attr("href", base_url + "/formgrader/manage_students/" + student + "/" + assignment)
                .text(name));
        } else {
            this.$student_name.text(name);
        }

        // student id
        this.$student_id.attr("data-order", student);
        this.$student_id.text(student);

        // timestamp
        var timestamp = this.model.get("timestamp");
        var display_timestamp = this.model.get("display_timestamp");
        if (timestamp === null) {
            timestamp = "None";
            display_timestamp = "None";
        }
        this.$timestamp.attr("data-order", timestamp);
        this.$timestamp.text(display_timestamp);

        // status
        if (!this.model.get("autograded")) {
            this.$status.attr("data-order", 0);
            this.$status.append($("<span/>")
                .addClass("label label-warning")
                .text("needs autograding"));
        } else if (this.model.get("needs_manual_grade")) {
            this.$status.attr("data-order", 1);
            this.$status.append($("<span/>")
                .addClass("label label-info")
                .text("needs manual grading"));
        } else {
            this.$status.attr("data-order", 2);
            this.$status.append($("<span/>")
                .addClass("label label-success")
                .text("graded"));
        }

        // score
        if (this.model.get("autograded")) {
            var score = roundToPrecision(this.model.get("score"), 2);
            var max_score = roundToPrecision(this.model.get("max_score"), 2);
            if (max_score === 0) {
                this.$score.attr("data-order", 0.0);
            } else {
                this.$score.attr("data-order", score / max_score);
            }
            this.$score.text(score + " / " + max_score);
        } else {
            this.$score.attr("data-order", 0.0);
        }

        // autograde
        this.$autograde.append($("<a/>")
            .attr("href", "#")
            .click(_.bind(this.autograde, this))
            .append($("<span/>")
                .addClass("glyphicon glyphicon-flash")
                .attr("aria-hidden", "true")));

        this.$autograde_all.append($("<a/>")
            .attr("href", "#")
            .click(_.bind(this.autograde_all, this))
            .append($("<span/>")
                .addClass("glyphicon glyphicon-flash")
                .attr("aria-hidden", "true")));

        // generate feedback
        this.$generate_feedback.append($("<a/>")
            .attr("href", "#")
            .click(_.bind(this.generate_feedback, this))
            .append($("<span/>")
                .addClass("glyphicon glyphicon-comment")
                .attr("aria-hidden", "true")));

        // release feedback
        this.$release_feedback.append($("<a/>")
            .attr("href", "#")
            .click(_.bind(this.release_feedback, this))
            .append($("<span/>")
                .addClass("glyphicon glyphicon-envelope")
                .attr("aria-hidden", "true")));
    },

    autograde_all: function () {
        this.clear();
    },

    autograde: function () {
        this.clear();
        this.$student_name.text("Please wait...");
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        $.post(base_url + "/formgrader/api/submission/" + assignment + "/" + student + "/autograde")
            .done(_.bind(this.autograde_success, this))
            .fail(_.bind(this.autograde_failure, this));
    },

    autograde_success: function (response) {
        this.model.fetch();
        response = JSON.parse(response);
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        if (response["success"]) {
            createLogModal(
                "success-modal",
                "Success",
                "Successfully autograded '" + assignment + "' for student '" + student + "'.",
                response["log"]);

        } else {
            createLogModal(
                "error-modal",
                "Error",
                "There was an error autograding '" + assignment + "' for student '" + student + "':",
                response["log"],
                response["error"]);
        }
    },

    autograde_failure: function (response) {
        this.model.fetch();
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        createModal(
            "error-modal",
            "Error",
            "There was an error autograding '" + assignment + "' for student '" + student + "'.");
    },

    generate_feedback: function () {
        this.clear();
        this.$student_name.text("Please wait...");
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        $.post(base_url + "/formgrader/api/assignment/" + assignment + "/" + student + "/generate_feedback")
            .done(_.bind(this.generate_feedback_success, this))
            .fail(_.bind(this.generate_feedback_failure, this));
    },

    generate_feedback_success: function (response) {
        this.model.fetch();
        response = JSON.parse(response);
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        if (response["success"]) {
            createLogModal(
                "success-modal",
                "Success",
                "Successfully generated feedback for '" + assignment + "' for student '" + student + "'.",
                response["log"]);

        } else {
            createLogModal(
                "error-modal",
                "Error",
                "There was an error generating feedback for '" + assignment + "' for student '" + student + "':",
                response["log"],
                response["error"]);
        }
    },

    generate_feedback_failure: function (response) {
        this.model.fetch();
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        createModal(
            "error-modal",
            "Error",
            "There was an error generating feedback for '" + assignment + "' for student '" + student + "'.");
    },

    release_feedback: function () {
        this.clear();
        this.$student_name.text("Please wait...");
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        $.post(base_url + "/formgrader/api/assignment/" + assignment + "/" + student + "/release_feedback")
            .done(_.bind(this.release_feedback_success, this))
            .fail(_.bind(this.release_feedback_failure, this));
    },

    release_feedback_success: function (response) {
        this.model.fetch();
        response = JSON.parse(response);
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        if (response["success"]) {
            createLogModal(
                "success-modal",
                "Success",
                "Successfully released feedback for '" + assignment + "' for student '" + student + "'.",
                response["log"]);

        } else {
            createLogModal(
                "error-modal",
                "Error",
                "There was an error releasing feedback for '" + assignment + "' for student '" + student + "':",
                response["log"],
                response["error"]);
        }
    },

    release_feedback_failure: function (response) {
        this.model.fetch();
        var student = this.model.get("student");
        var assignment = this.model.get("name");
        createModal(
            "error-modal",
            "Error",
            "There was an error releasing feedback for '" + assignment + "' for student '" + student + "'.");
    },

});

var insertRow = function (table) {
    var row = $("<tr/>");
    row.append($("<td/>").addClass("student-name"));
    row.append($("<td/>").addClass("text-center student-id"));
    row.append($("<td/>").addClass("text-center timestamp"));
    row.append($("<td/>").addClass("text-center status"));
    row.append($("<td/>").addClass("text-center score"));
    row.append($("<td/>").addClass("text-center autograde"));
    row.append($("<td/>").addClass("text-center generate-feedback"));
    row.append($("<td/>").addClass("text-center release-feedback"));
    table.append(row)
    return row;
};

var loadSubmissions = function () {
    var tbl = $("#main-table");

    models = new Submissions();
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                var view = new SubmissionUI({
                    "model": model,
                    "el": insertRow(tbl)
                });
                views.push(view);
            });
            insertDataTable(tbl.parent());
            models.loaded = true;
        }
    });
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }  

function autograde_all() {
    var auto = $('#autograde_all');
    auto.addClass("autograde_all")
    .append("Autograde All: ").append($("<a/>")
        .click(function(e){
              $.ajax({
                url: base_url + '/formgrader/api/autograde_all',
                type: 'get',
                data: {
                  'assignment_id' : assignment_id
                },
                success: function(response) {
                    console.log(response);
                },
                error: function(e) {
                    console.log(e);
                },
                async: false
              }); 
              async_progress();
        })
        .attr("href", "#")
        .append($("<span/>")
        .addClass("glyphicon glyphicon-flash")
        .attr("aria-hidden", "true")));
}

async function async_progress() {
    var result;
    var progress_bar = $('#progress_bar');
    var progress_value = $('#progress');
    var autograde_icon = $('#autograde_all');
    var autograde_percentage = $('#autograde_percentage');
    var autograde_cell_div = $('#autograde_cell');
    var autograde_log = $('#autograde_log');
    var log_time = $('#log_time');
    var tbl = $("#main-table");
    var flag = 0;
    log_time.click(function(e){
        $.ajax({
          url: base_url + '/formgrader/api/autograding_log',
          type: 'get',
          data: {
            'assignment_id' : assignment_id
          },
          success: function(response) {
              try{
                var log_report = JSON.parse(JSON.parse(response)['autograde_log']);
                var student = Object.keys(log_report);
                report = '';
                for (var i = 0; i < student.length; i++){
                    if (student[i] != 'time') {
                        report += '\n' + student[i] + ': \n';  
                        report += log_report[student[i]];
                    }
                }
                createLogModal(
                "log-modal",
                "Autograde Log",
                "Autograded notebooks for \'" + assignment_id + "\'.",
                report);
              }catch{
                console.log(response);
              }
          },
          error: function(e) {
              console.log(e);
          },
          async: false
        });
    });
    while(true){
        try {
            result = await $.ajax({
                url: base_url + '/formgrader/api/autograding_progress',
                type: 'get',
                data: {
                    'assignment_id' : assignment_id
                  },
            });
            var progress = JSON.parse(result);
            var autograde_progress = parseInt(progress['autograde_idx']) * 100 / parseInt(progress['autograde_total']);
            if (progress['autograde_flag'] == 0){
                if (flag == 1){
                    flag = 0;
                    console.log('Restart!');
                    location.reload()
                }
                if (progress['autograde_log'] == 'Autograding required.'){
                    autograde_cell_div.hide();
                }else{
                    autograde_cell_div.show();
                }
                autograde_log.show();
                log_time.html(progress['autograde_log']);
                progress_bar.hide();
                autograde_icon.show();
                progress_value.hide();
                tbl.show();
                break;
            }
            else{
                flag = 1;
                autograde_log.hide();
                tbl.hide();
                autograde_icon.hide();
                autograde_cell_div.hide();
                if (progress['autograde_assignment'] == assignment_id){
                    progress_bar.show();
                    progress_value.show();
                    autograde_percentage.html('Autograding progress: ' + autograde_progress.toFixed(0).toString() + '%');
                    progress_value.val(autograde_progress);
                }else{
                    progress_bar.show();
                    progress_value.hide();
                    autograde_percentage.html('\'' + progress['autograde_assignment'] + '\' autograding in progress. Please wait...');
                }
            }
        } catch (error) {
            console.error(error);
            break;
        }
        await sleep(1000);
    }
}

var models = undefined;
var views = [];
$(window).on('load', function () {
    autograde_all();
    loadSubmissions();
    async_progress();
});