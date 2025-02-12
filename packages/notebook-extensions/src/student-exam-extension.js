import $ from "jquery";
import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { initialize_cell_extension } from "@e2xgrader/cell-extension";
import { AssignmentViewToolbar } from "@e2xgrader/assignment-view-celltoolbar";
import { patch_assignment_notebook } from "@e2xgrader/restricted-assignment-notebook";
import { disable_shortcuts } from "@e2xgrader/restricted-exam-notebook";
import { ExamMenubar } from "@e2xgrader/exam-menubar";
import { username } from "@e2xgrader/utils";

function initialize() {
  initialize_cell_extension();
  patch_assignment_notebook();
  new ExamMenubar().activate();
  new AssignmentViewToolbar().activate();
  disable_shortcuts();
  username.add_username();
  $("#notebook_name").off("click");
  $("#rename_notebook").hide();
}

export function load_ipython_extension() {
  if (Jupyter.notebook?._fully_loaded) {
    initialize();
  } else {
    events.on("notebook_loaded.Notebook", initialize);
  }
}
