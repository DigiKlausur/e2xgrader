import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { initialize_cell_extension } from "@e2xgrader/cell-extension";
import { CreateAssignmentToolbar } from "@e2xgrader/create-assignment-celltoolbar";
import { TaskMenubar, TemplateMenubar } from "@e2xgrader/authoring-menubar";

function is_taskbook() {
  let metadata = Jupyter.notebook.metadata;
  return (
    metadata.hasOwnProperty("nbassignment") &&
    metadata.nbassignment.hasOwnProperty("type") &&
    metadata.nbassignment.type === "task"
  );
}

function is_templatebook() {
  let metadata = Jupyter.notebook.metadata;
  return (
    metadata.hasOwnProperty("nbassignment") &&
    metadata.nbassignment.hasOwnProperty("type") &&
    metadata.nbassignment.type === "template"
  );
}

function initialize() {
  initialize_cell_extension();

  const celltoolbar = new CreateAssignmentToolbar();
  celltoolbar.register();

  console.log("Are we a taskbook?");
  console.log(Jupyter.notebook.metadata);
  console.log(is_taskbook());

  if (is_taskbook()) {
    celltoolbar.activate();
    new TaskMenubar().activate();
  } else if (is_templatebook()) {
    celltoolbar.activate();
    new TemplateMenubar().activate();
  }
}

export function load_ipython_extension() {
  if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
    initialize();
  } else {
    events.on("notebook_loaded.Notebook", initialize());
  }
}
