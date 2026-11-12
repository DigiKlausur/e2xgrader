import "./assignment-list.css";
import $ from "jquery";
import Jupyter from "base/js/namespace";
import { AssignmentList, CourseList } from "./assignment-list";

function create_panel(name, heading, placeholder, attributes = "") {
  return `
    <div class="panel panel-default">
      <div class="panel-heading">${heading}</div>
      <div class="panel-body">
        <div id="${name}_assignments_list" class="list_container" ${attributes}>
          <div id="${name}_assignments_list_placeholder" class="row list_placeholder">
            <div>${placeholder}</div>
          </div>
          <div id="${name}_assignments_list_loading" class="row list_loading">
            <div>Loading, please wait...</div>
          </div>
          <div id="${name}_assignments_list_error" class="row list_error">
            <div></div>
          </div>
        </div>
      </div>
    </div>`;
}

function create_tab() {
  return $(`
    <div id="assignments" class="tab-pane">
      <div id="assignments_toolbar" class="row list_toolbar">
        <div class="col-sm-8 no-padding">
          <span id="assignments_list_info" class="toolbar_info">
            Released, downloaded, and submitted assignments for course:
          </span>
          <div class="btn-group btn-group-xs">
            <button type="button" class="btn btn-default" id="course_list_default">
              Loading, please wait...
            </button>
            <button type="button" class="btn btn-default dropdown-toggle"
                id="course_list_dropdown" data-toggle="dropdown"
                aria-haspopup="true" aria-expanded="false" disabled="disabled">
              <span class="caret"></span>
              <span class="sr-only">Toggle Dropdown</span>
            </button>
            <ul class="dropdown-menu" id="course_list"></ul>
          </div>
        </div>
        <div class="col-sm-4 no-padding tree-buttons">
          <span id="assignments_buttons" class="pull-right toolbar_buttons">
            <button id="refresh_assignments_list" title="Refresh assignments list"
                class="btn btn-default btn-xs">
              <i class="fa fa-refresh"></i>
            </button>
          </span>
        </div>
      </div>
      <div class="panel-group">
        ${create_panel(
          "released",
          "Released assignments",
          "There are no assignments to fetch."
        )}
        ${create_panel(
          "fetched",
          "Downloaded assignments",
          "There are no downloaded assignments.",
          'role="tablist" aria-multiselectable="true"'
        )}
        ${create_panel(
          "submitted",
          "Submitted assignments",
          "There are no submitted assignments."
        )}
      </div>
    </div>`);
}

export function load_assignment_list() {
  if (!Jupyter.notebook_list) {
    return;
  }
  const base_url = Jupyter.notebook_list.base_url;
  $(".tab-content").append(create_tab());

  const assignment_list = new AssignmentList(
    "#released_assignments_list",
    "#fetched_assignments_list",
    "#submitted_assignments_list",
    base_url
  );
  const course_list = new CourseList(
    "#course_list",
    "#course_list_default",
    "#course_list_dropdown",
    "#refresh_assignments_list",
    assignment_list,
    base_url
  );

  $("#tabs").append(
    $("<li/>").append(
      $("<a/>")
        .attr("href", "#assignments")
        .attr("data-toggle", "tab")
        .text("Assignments")
        .on("click", () => {
          window.history.pushState(null, null, "#assignments");
          course_list.load_list();
        })
    )
  );
}
