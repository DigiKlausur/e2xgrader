import $ from "jquery";
import Jupyter from "base/js/namespace";
import utils from "base/js/utils";
import dialog from "base/js/dialog";

export class Submit {
  constructor() {
    this.courses = [];
    this.assignment = undefined;
    this.base_url = Jupyter.notebook.base_url;
    this.name = Jupyter.notebook.notebook_name.split(".ipynb")[0];
    let url = window.location.href.split("/");
    this.assignment_id = url[url.length - 2];
    this.get_courses();
  }

  get_courses() {
    let that = this;
    let settings = {
      processData: false,
      cache: false,
      type: "GET",
      dataType: "json",
      success: function (data, status, xhr) {
        if (data.success) {
          that.courses = data.value;
          that.courses.forEach(function (course) {
            that.get_fetched_assignments(course);
          });
        }
      },
      error: function (data, status, xhr) {
        console.log("Error fetching courses");
      },
    };

    let url = utils.url_path_join(this.base_url, "courses");
    utils.ajax(url, settings);
  }

  get_fetched_assignments(course) {
    let that = this;
    let settings = {
      cache: false,
      type: "GET",
      dataType: "json",
      data: {
        course_id: course,
      },
      success: function (data, status, xhr) {
        if (data.success) {
          data.value.forEach(function (assignment) {
            if (
              assignment.status === "fetched" &&
              assignment.assignment_id === that.assignment_id
            ) {
              that.assignment = assignment;
              $("#submit").show();
            }
          });
        }
      },
      error: function (data, status, xhr) {
        console.log("Error");
        console.log(data);
      },
    };

    let url = utils.url_path_join(this.base_url, "assignments");
    utils.ajax(url, settings);
  }

  disable_submit_button() {
    $(".e2x-submit").off("click");
    $(".e2x-submit").css("background-color", "gray");
  }

  enable_submit_button() {
    let that = this;
    $(".e2x-submit").on("click", function () {
      that.prepare_submit();
    });
    $(".e2x-submit").css("background-color", "");
  }

  prepare_submit() {
    let that = this;
    // Save
    Jupyter.notebook
      .save_checkpoint()
      .then(function () {
        that.disable_submit_button();
        that.submit_spinner();
        that.submit();
      })
      .catch(function (error) {
        that.submit_error_modal();
      });
  }

  submit_spinner() {
    $("html").append(
      $("<div/>")
        .attr("id", "submitting")
        .append(
          $("<div/>")
            .attr("id", "submitting_box")
            .append(
              $("<i/>")
                .addClass("fa fa-spinner fa-spin")
                .attr("id", "submit_spinner")
            )
            .append(
              $("<p/>").text("Submitting exam. This may take a few seconds...")
            )
        )
    );
  }

  submit() {
    if (this.assignment) {
      let settings = {
        cache: false,
        type: "POST",
        dataType: "json",
        data: {
          course_id: this.assignment.course_id,
          assignment_id: this.assignment.assignment_id,
        },
        success: this.submit_success_modal.bind(this),
        error: this.handle_submit_error.bind(this),
      };
      let url = utils.url_path_join(this.base_url, "assignments", "submit");
      utils.ajax(url, settings);
    }
  }

  handle_submit_error(data, status, xhr) {
    console.log("Error submitting");
  }

  submit_error_modal(data) {
    $("#submitting").remove();
    this.enable_submit_button();

    let body = $("<div/>");
    body.append(
      $("<h4/>").text("Something went wrong while submitting the assignment")
    );
    body.append(
      $("<p/>").append(
        "Please try to submit via the assignments tab or contact a supervisor."
      )
    );

    dialog.modal({
      keyboard_manager: Jupyter.keyboard_manager,
      title: "Error submitting assignment!",
      body: body,
      buttons: {
        OK: {},
      },
    });
  }

  submit_success_modal(data) {
    $("#submitting").remove();
    this.enable_submit_button();
    console.log(data);

    let body = $("<div/>");

    body.append($("<h4/>").text("We have received your submission on:"));
    body.append($("<pre/>").text(data["timestamp"].split(".")[0]));

    body.append($("<h4/>").text("Do you want to end your exam now?"));
    body.append(
      $("<p/>")
        .append("You will receive your ")
        .append($("<span/>").append("hashcode").attr("id", "hashcode_label"))
        .append(" when you end the exam.")
    );

    dialog.modal({
      keyboard_manager: Jupyter.keyboard_manager,
      title: "Exam has been submitted successfully!",
      body: body,
      buttons: {
        "No, continue working on the exam": {
          class: "btn-warning",
        },
        "Yes, exit the exam": {
          click: function () {
            window.location.href = utils.url_path_join(
              Jupyter.notebook.base_url,
              "view",
              Jupyter.notebook.notebook_path.replace(".ipynb", "_hashcode.html")
            );
          },
          class: "btn-success",
        },
      },
    });
  }
}
