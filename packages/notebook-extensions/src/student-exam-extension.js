import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { initialize_cell_extension } from "@e2xgrader/cell-extension";
import { AssignmentViewToolbar } from "@e2xgrader/assignment-view-celltoolbar";
import { patch_assignment_notebook } from "@e2xgrader/restricted-assignment-notebook";
import { disable_shortcuts } from "@e2xgrader/restricted-exam-notebook";
import { ExamMenubar } from "@e2xgrader/exam-menubar";

function initialize() {
  initialize_cell_extension();
  patch_assignment_notebook();
  new ExamMenubar().activate();
  let toolbar = new AssignmentViewToolbar();
  toolbar.register();
  toolbar.activate();
  disable_shortcuts();
}

export function load_ipython_extension() {
  if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
    initialize();
  } else {
    events.on("notebook_loaded.Notebook", initialize);
  }
}
