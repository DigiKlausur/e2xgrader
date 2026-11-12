// Ported from the nbgrader 0.8 assignment_list nbextension.
// The server side (/courses, /assignments) is still provided by nbgrader.
import $ from "jquery";
import utils from "base/js/utils";
import dialog from "base/js/dialog";
import { show_validation_results } from "@e2xgrader/validate-assignment";

// Notebook >= 4.3.1 uses xsrf; its ajax sends the token in the header
const ajax = utils.ajax || $.ajax;

// The action button shown for an assignment, by assignment status
const ACTIONS = {
  released: {
    name: "fetch",
    label: "Fetch",
    running: "Fetching...",
    error: "Error fetching assignment.",
  },
  fetched: {
    name: "submit",
    label: "Submit",
    running: "Submitting...",
    error: "Error submitting assignment.",
  },
  submitted: {
    name: "fetch_feedback",
    label: "Fetch Feedback",
    running: "Fetching Feedback...",
    error: "Error fetching feedback.",
  },
};

function show_submit_error(data) {
  const body = $("<div/>")
    .attr("id", "submission-message")
    .append(
      $("<div/>").append($("<p/>").text("Assignment not submitted:")),
      $("<pre/>").text(data.value)
    );
  dialog.modal({
    title: "Invalid Submission",
    body: body,
    buttons: { OK: { class: "btn-primary" } },
  });
}

function rotate_icon(icon, degrees) {
  // jQuery can't animate rotations, so animate an unused css property
  // (borderSpacing) and apply its value as the rotation on every step
  const step = (now) => icon.css("transform", `rotate(-${now}deg)`);
  icon.animate({ borderSpacing: degrees }, { duration: 250, step });
}

function add_collapse_arrow(link) {
  const icon = $("<i/>")
    .addClass("fa fa-caret-down")
    .css("transform", "rotate(-90deg)")
    .css("borderSpacing", "90")
    .css("margin-left", "3px");
  link.append(icon);
  let expanded = false;
  link.on("click", () => {
    expanded = !expanded;
    rotate_icon(icon, expanded ? 0 : 90);
  });
}

// A row in the collapsible list below a fetched or submitted assignment
function make_child_row(name, status) {
  const columns = $("<div/>")
    .addClass("col-md-12")
    .append(name, $("<span/>").addClass("item_course col-sm-2"), status);
  return $("<div/>").addClass("list_item row").append(columns);
}

function make_child_list(id, rows, collapsed) {
  return $("<div/>")
    .attr("id", id)
    .attr("role", "tabpanel")
    .addClass("panel-collapse list_container assignment-notebooks")
    .toggleClass("collapse", collapsed)
    .append($("<div/>").addClass("list_item row"), rows);
}

function make_submission_row(submission, base_url) {
  const name = $("<span/>")
    .addClass("item_name col-sm-6")
    .append($("<span/>").text(submission.timestamp));
  if (submission.has_local_feedback && !submission.feedback_updated) {
    const url = utils.url_path_join(
      base_url,
      "tree",
      submission.local_feedback_path
    );
    name.append(
      $("<a/>")
        .attr("href", url)
        .attr("target", "_blank")
        .text(" (view feedback)")
    );
  } else if (submission.has_exchange_feedback) {
    name.append($("<span/>").text(" (feedback available to fetch)"));
  }
  return make_child_row(name, $("<span/>").addClass("item_status col-sm-4"));
}

function make_validate_button(path, base_url) {
  const container = $("<span/>").addClass("item_status col-sm-4");
  const button = $("<button/>")
    .addClass("btn btn-default btn-xs")
    .text("Validate");
  button.on("click", () => {
    button.text("Validating...").attr("disabled", "disabled");
    ajax(utils.url_path_join(base_url, "assignments", "validate"), {
      cache: false,
      type: "POST",
      dataType: "json",
      data: { path },
      success: (data) => {
        const passed = show_validation_results(data);
        button
          .text("Validate")
          .removeAttr("disabled")
          .removeClass("btn-default btn-success btn-danger")
          .addClass(passed ? "btn-success" : "btn-danger");
      },
      error: (xhr, status, error) => {
        container.empty().text("Error validating assignment.");
        utils.log_ajax_error(xhr, status, error);
      },
    });
  });
  return container.append(button);
}

function make_notebook_row(notebook, base_url) {
  const url = utils.url_path_join(
    base_url,
    "tree",
    utils.url_join_encode(notebook.path)
  );
  const link = $("<a/>")
    .attr("href", url)
    .attr("target", "_blank")
    .text(notebook.notebook_id);
  const name = $("<span/>").addClass("item_name col-sm-6").append(link);
  return make_child_row(name, make_validate_button(notebook.path, base_url));
}

class Assignment {
  constructor(data, parent_selector, on_refresh, base_url) {
    this.data = data;
    this.parent_selector = parent_selector;
    this.on_refresh = on_refresh;
    this.base_url = base_url;
    this.element = $("<div/>")
      .addClass("list_item row")
      .append(this.make_row(), this.make_children());
  }

  escape_id() {
    // Prefix with "nbgrader" so the id always starts with a letter, then
    // drop characters that are invalid in HTML ids
    const id = `nbgrader-${this.data.course_id}-${this.data.assignment_id}`;
    return id.replace(/ /g, "_").replace(/[^A-Za-z0-9\-_]/g, "");
  }

  make_row() {
    const course = $("<span/>")
      .addClass("item_course col-sm-2")
      .text(this.data.course_id);
    return $("<div/>")
      .addClass("col-md-12")
      .append(this.make_link(), course, this.make_button());
  }

  make_link() {
    const container = $("<span/>").addClass("item_name col-sm-6");
    if (this.data.status !== "fetched") {
      return container.append($("<span/>").text(this.data.assignment_id));
    }
    const id = this.escape_id();
    const link = $("<a/>")
      .addClass("collapsed assignment-notebooks-link")
      .attr({
        role: "button",
        "data-toggle": "collapse",
        "data-parent": this.parent_selector,
        href: `#${id}`,
        "aria-expanded": "false",
        "aria-controls": id,
      })
      .text(this.data.assignment_id);
    add_collapse_arrow(link);
    return container.append(link);
  }

  make_children() {
    if (this.data.status === "submitted") {
      const rows = this.data.submissions.map((submission) =>
        make_submission_row(submission, this.base_url)
      );
      return make_child_list(`${this.escape_id()}-submissions`, rows, false);
    }
    if (this.data.status === "fetched") {
      const rows = this.data.notebooks.map((notebook) =>
        make_notebook_row(notebook, this.base_url)
      );
      return make_child_list(this.escape_id(), rows, true);
    }
    return null;
  }

  make_button() {
    const container = $("<span/>").addClass("item_status col-sm-4");
    const action = ACTIONS[this.data.status];
    if (action === undefined) {
      return container;
    }
    const button = $("<button/>")
      .addClass("btn btn-primary btn-xs")
      .text(action.label);
    button.on("click", () => {
      button.text(action.running).attr("disabled", "disabled");
      ajax(utils.url_path_join(this.base_url, "assignments", action.name), {
        cache: false,
        type: "POST",
        dataType: "json",
        data: {
          course_id: this.data.course_id,
          assignment_id: this.data.assignment_id,
        },
        success: (response) => {
          // A rejected submission is shown in a dialog and the list is kept
          if (action.name === "submit" && !response.success) {
            show_submit_error(response);
            button.text(action.label).removeAttr("disabled");
          } else {
            this.on_refresh(response);
          }
        },
        error: (xhr, status, error) => {
          container.empty().text(action.error);
          utils.log_ajax_error(xhr, status, error);
        },
      });
    });
    return container.append(button);
  }
}

export class AssignmentList {
  constructor(
    released_selector,
    fetched_selector,
    submitted_selector,
    base_url
  ) {
    this.fetched_selector = fetched_selector;
    // The list each assignment is shown in, by assignment status
    this.lists = {
      released: $(released_selector),
      fetched: $(fetched_selector),
      submitted: $(submitted_selector),
    };
    this.base_url = base_url;
    this.callback = undefined;
  }

  load_list(course, callback) {
    this.callback = callback;
    this.clear_list(true);
    ajax(utils.url_path_join(this.base_url, "assignments"), {
      cache: false,
      type: "GET",
      dataType: "json",
      data: { course_id: course },
      success: (data) => this.handle_load_list(data),
      error: utils.log_ajax_error,
    });
  }

  clear_list(loading = false) {
    Object.values(this.lists).forEach((list) => {
      list.children(".list_item").remove();
      list.children(".list_loading").toggle(loading);
      list.children(".list_placeholder").toggle(!loading);
      list.children(".list_error").hide();
    });
  }

  show_error(error) {
    Object.values(this.lists).forEach((list) => {
      list.children(".list_item").remove();
      list.children(".list_error").text(error).show();
      list.children(".list_loading").hide();
      list.children(".list_placeholder").hide();
    });
  }

  handle_load_list(data) {
    if (data.success) {
      this.load_list_success(data.value);
    } else {
      this.show_error(data.value);
    }
  }

  load_list_success(assignments) {
    this.clear_list();
    assignments.forEach((data) => {
      const list = this.lists[data.status];
      if (list === undefined) {
        return;
      }
      const assignment = new Assignment(
        data,
        this.fetched_selector,
        (response) => this.handle_load_list(response),
        this.base_url
      );
      list.append(assignment.element);
      list.children(".list_placeholder").hide();
    });

    if (this.callback) {
      this.callback();
      this.callback = undefined;
    }
  }
}

export class CourseList {
  constructor(
    course_list_selector,
    default_course_selector,
    dropdown_selector,
    refresh_selector,
    assignment_list,
    base_url
  ) {
    this.course_list_element = $(course_list_selector);
    this.default_course_element = $(default_course_selector);
    this.dropdown_element = $(dropdown_selector);
    this.assignment_list = assignment_list;
    this.base_url = base_url;
    this.current_course = undefined;
    this.data = undefined;
    $(refresh_selector).on("click", () => this.load_list());
  }

  enable_list() {
    this.dropdown_element.removeAttr("disabled");
  }

  disable_list() {
    this.dropdown_element.attr("disabled", "disabled");
  }

  clear_list() {
    this.course_list_element.children("li").remove();
  }

  load_list() {
    this.disable_list();
    this.clear_list();
    this.assignment_list.clear_list(true);
    ajax(utils.url_path_join(this.base_url, "courses"), {
      processData: false,
      cache: false,
      type: "GET",
      dataType: "json",
      success: (data) => this.handle_load_list(data),
      error: utils.log_ajax_error,
    });
  }

  handle_load_list(data) {
    if (data.success) {
      this.load_list_success(data.value);
    } else {
      this.default_course_element.text("Error fetching courses!");
      this.enable_list();
      this.assignment_list.show_error(data.value);
    }
  }

  load_list_success(courses) {
    this.data = courses;
    this.disable_list();
    this.clear_list();

    if (courses.length === 0) {
      this.default_course_element.text("No courses found.");
      this.assignment_list.clear_list();
      this.enable_list();
      return;
    }

    // Reload the current course to refresh its assignments, unless it is gone
    const course = courses.includes(this.current_course)
      ? this.current_course
      : courses[0];
    this.change_course(course);
  }

  change_course(course) {
    this.disable_list();
    this.current_course = course;
    this.default_course_element.text(course);
    this.assignment_list.load_list(course, () =>
      this.load_assignment_list_success()
    );
  }

  load_assignment_list_success() {
    // Fill the course dropdown once, after the first assignment list loaded
    if (this.data) {
      this.data.forEach((course) => {
        const element = $("<li/>").append(
          $("<a/>").attr("href", "#").text(course)
        );
        element.on("click", () => this.change_course(course));
        this.course_list_element.append(element);
      });
      this.data = undefined;
    }
    this.enable_list();
  }
}
