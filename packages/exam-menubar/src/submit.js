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

  prepare_submit() {
    let that = this;
    // Save
    Jupyter.notebook
      .save_checkpoint()
      .then(function () {
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
          $("<i/>")
            .addClass("fa fa-spinner fa-spin")
            .attr("id", "submit_spinner")
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
        success: this.submit_success_modal,
        error: this.handle_submit_error,
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
    console.log(data);
    let hashcode_html =
      window.location.href.split(".ipynb")[0] + "_hashcode.html";
    let body = $("<div/>");

    body.append($("<h4/>").text("Your Timestamp:"));
    body.append($("<pre/>").text(data["timestamp"].split(".")[0]));

    if (data.hasOwnProperty("hashcode") && data.hashcode.length > 0) {
      body.append($("<h4/>").text("Your Hashcode:"));
      body.append($("<pre/>").text(data["hashcode"]));

      body.append(
        $("<p/>")
          .append("You can verify your submission ")
          .append($("<a/>").attr("href", hashcode_html).text("here"))
          .append(".")
      );
    }

    dialog.modal({
      keyboard_manager: Jupyter.keyboard_manager,
      title: "Assignment has been successfully submitted!",
      body: body,
      buttons: {
        OK: {},
      },
    });
  }
}
