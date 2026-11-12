// Ported from the nbgrader 0.8 validate_assignment nbextension.
// The server side (/assignments/validate) is still provided by nbgrader.
import $ from "jquery";
import Jupyter from "base/js/namespace";
import dialog from "base/js/dialog";
import utils from "base/js/utils";

// Notebook >= 4.3.1 uses xsrf; its ajax sends the token in the header
const ajax = utils.ajax || $.ajax;

function paragraph(text) {
  return $("<div/>").append($("<p/>").text(text));
}

function append_cells(body, message, cells) {
  cells.forEach((cell) => {
    body.append(paragraph(message(cell)), $("<pre/>").text(cell.source));
  });
}

function create_result_body(data) {
  const body = $("<div/>").attr("id", "validation-message");
  if (data.success !== true) {
    body.append(
      paragraph("There was an error running the validate command:"),
      $("<pre/>").text(data.value)
    );
    return body;
  }

  const result =
    typeof data.value === "string" ? JSON.parse(data.value) : data.value;

  if (result.type_changed !== undefined) {
    append_cells(
      body,
      (cell) =>
        `The following ${cell.old_type} cell has changed to a ` +
        `${cell.new_type} cell, but it should not have!`,
      result.type_changed
    );
    body.addClass("validation-type-changed");
  } else if (result.changed !== undefined) {
    append_cells(
      body,
      () =>
        "The source of the following cell has changed, but it should not have!",
      result.changed
    );
    body.addClass("validation-changed");
  } else if (result.passed !== undefined) {
    append_cells(body, () => "The following cell passed:", result.passed);
    body.addClass("validation-passed");
  } else if (result.failed !== undefined) {
    result.failed.forEach((cell) => {
      body.append(
        paragraph("The following cell failed:"),
        $("<pre/>").text(cell.source),
        $("<pre/>").html(cell.error)
      );
    });
    body.addClass("validation-failed");
  } else {
    body.append(paragraph("Success! Your notebook passes all the tests."));
    body.addClass("validation-success");
  }
  return body;
}

function show_results(data) {
  dialog.modal({
    title: "Validation Results",
    body: create_result_body(data),
    buttons: { OK: { class: "btn-primary" } },
  });
}

function validate_notebook(button) {
  Jupyter.notebook.save_notebook().then(() => {
    button.text("Validating...").attr("disabled", "disabled");
    ajax(
      utils.url_path_join(Jupyter.notebook.base_url, "assignments", "validate"),
      {
        cache: false,
        type: "POST",
        dataType: "json",
        data: { path: Jupyter.notebook.notebook_path },
        success: show_results,
        error: utils.log_ajax_error,
        complete: () => button.text("Validate").removeAttr("disabled"),
      }
    );
  });
}

export function add_validate_button() {
  const button = $("<button/>")
    .addClass("btn btn-default validate")
    .text("Validate");
  button.on("click", () => validate_notebook(button));
  $("#maintoolbar-container").append(
    $("<div/>").addClass("btn-group").append(button)
  );
}
