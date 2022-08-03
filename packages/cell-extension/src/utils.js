import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { Notebook } from "notebook/js/notebook";
import { TextCell } from "notebook/js/textcell";
import { MarkdownCell } from "notebook/js/textcell";
import { utils, cells } from "@e2xgrader/cells";

// Flag to check if we are creating an assignment or not
let edit_mode = false;

const old_render = MarkdownCell.prototype.render;
const old_to_markdown = Notebook.prototype.to_markdown;
const old_toJSON = TextCell.prototype.toJSON;
const old_unrender = MarkdownCell.prototype.unrender;

/**
 * Overwrite the original to_markdown function
 * If an extra cell is turned from code to markdown
 * we need to make sure to unrender it fully
 */
export function patch_Notebook_to_markdown() {
  Notebook.prototype.to_markdown = function () {
    old_to_markdown.apply(this, arguments);
    let cell = this.get_cell(arguments[0]);
    cell.unrender_force();
    cell.render();
  };
}

/**
 * Overwrite the original toJSON function
 * If we have an attachment cell we want to keep all attachments
 * independent of whether they are referenced in the cell source
 * or not.
 */
export function patch_TextCell_toJSON() {
  TextCell.prototype.toJSON = function () {
    if (utils.get_e2x_cell_type(this) == "attachments") {
      // Do not remove ununsed attachments
      arguments[0] = false;
      return old_toJSON.apply(this, arguments);
    } else {
      return old_toJSON.apply(this, arguments);
    }
  };
}

/**
 * Listen to changes of the celltoolbar to determine if we are in edit mode or not
 */
function listen_to_edit_mode_changes() {
  if (
    Jupyter.notebook.metadata.hasOwnProperty("celltoolbar") &&
    Jupyter.notebook.metadata.celltoolbar === "Create Assignment"
  ) {
    edit_mode = true;
  }
  events.on("preset_activated.CellToolbar", function (evt, preset) {
    if (preset.name == "Create Assignment") {
      edit_mode = true;
    } else {
      edit_mode = false;
    }
    render_e2x_cells();
  });
  events.on("global_hide.CellToolbar", function (evt, instance) {
    edit_mode = false;
    render_e2x_cells();
  });
}

/**
 * Overwrite the original render function of markdown cells
 */
export function patch_MarkdownCell_render() {
  MarkdownCell.prototype.render_force = old_render;
  MarkdownCell.prototype.render = function () {
    let type = utils.get_e2x_cell_type(this);
    if (cells.hasOwnProperty(type)) {
      let e2x_cell = new cells[type](this);
      e2x_cell.edit_mode = edit_mode;
      e2x_cell.render();
    } else {
      old_render.apply(this, arguments);
    }
  };
  listen_to_edit_mode_changes();
}

/**
 * Overwrite the original unrender function of markdown cells
 * Disables unrendering e2x cells
 */
export function patch_MarkdownCell_unrender() {
  MarkdownCell.prototype.unrender_force = old_unrender;
  MarkdownCell.prototype.unrender = function () {
    if (!utils.is_e2x(this)) {
      old_unrender.apply(this, arguments);
    }
  };
}

/**
 * Iterate over all cells and rerender extra cells
 */
export function render_e2x_cells() {
  let cells = Jupyter.notebook.get_cells();
  for (let i in cells) {
    let cell = cells[i];
    if (utils.is_e2x(cell) && cell.cell_type === "markdown" && cell.rendered) {
      cell.unrender_force();
      cell.render();
    }
  }
}
