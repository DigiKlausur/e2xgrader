import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { initialize_cell_extension } from "@e2xgrader/cell-extension";
import { AssignmentViewToolbar } from "@e2xgrader/assignment-view-celltoolbar";
import { patch_assignment_notebook } from "@e2xgrader/restricted-assignment-notebook";

function initialize() {
  initialize_cell_extension();
  patch_assignment_notebook();
  new AssignmentViewToolbar().register();
}

export function load_ipython_extension() {
  if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
    initialize();
  } else {
    events.on("notebook_loaded.Notebook", initialize);
  }
}
