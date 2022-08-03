import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { initialize_cell_extension } from "@e2xgrader/cell-extension";
import { CreateAssignmentToolbar } from "@e2xgrader/create-assignment-celltoolbar";

function initialize() {
  initialize_cell_extension();
  new CreateAssignmentToolbar().register();
}

export function load_ipython_extension() {
  events.on("notebook_loaded.Notebook", initialize());
  if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
    initialize();
  }
}
