import $ from "jquery";
import Jupyter from "base/js/namespace";
import dialog from "base/js/dialog";
import { utils } from "@e2xgrader/utils";
import { Notebook } from "notebook/js/notebook";
import { Cell } from "notebook/js/cell";

const old_to_code = Notebook.prototype.to_code;
const old_to_markdown = Notebook.prototype.to_markdown;
const old_to_raw = Notebook.prototype.to_raw;
const old_move_cell_down = Notebook.prototype.move_cell_down;
const old_move_selection_down = Notebook.prototype.move_selection_down;
const old_move_cell_up = Notebook.prototype.move_cell_up;
const old_move_selection_up = Notebook.prototype.move_selection_up;
const old_paste_cell_replace = Notebook.prototype.paste_cell_replace;
const old_paste_cell_above = Notebook.prototype.paste_cell_above;
const old_paste_cell_below = Notebook.prototype.paste_cell_below;

/**
 * Display a dialog informing the user that they can not move nbgrader cells
 */
function alert_move_cell_disabled() {
  let body = $("<div/>").append(
    $("<span/>").text(
      "At least one of the selected cells belongs to the assignment and can not be moved!"
    )
  );
  dialog.modal({
    keyboard_manager: Jupyter.keyboard_manager,
    title: "Can not move cells",
    body: body,
    buttons: {
      OK: {},
    },
  });
}

/**
 * Display a dialog informing the user that they can not change the type of nbgrader cells
 */
function alert_cell_type_select_blocked() {
  let body = $("<div/>").append(
    $("<span/>").text(
      "You can not change the type of a cell that belongs to the assignment!"
    )
  );
  dialog.modal({
    keyboard_manager: Jupyter.keyboard_manager,
    title: "Can not change cell type",
    body: body,
    buttons: {
      OK: {},
    },
  });
}

/**
 * Remove all nbgrader cells from the clipboard to prevent pasting them
 *
 * @params  {Object[]} clipboard
 * @returns {Object[]} sanitized clipboard
 */
function sanitize_clipboard(clipboard) {
  if (clipboard === null) {
    return clipboard;
  }
  let sanitized = [];
  clipboard.forEach(function (cell) {
    if (!utils.is_nbgrader(cell)) {
      sanitized.push(cell);
    }
  });
  if (sanitized.length == 0) {
    return null;
  }
  return sanitized;
}

/**
 * Check if any cell is a nbgrader cell and display a warning
 *
 * @param  {Cell[]}  cells - array of cells to check
 * @return {Boolean} `true` if no nbgrader cell is in the array
 */
function validate_move_cells(cells) {
  let nbgrader_cell_selected = false;
  cells.some(function (cell) {
    if (utils.is_nbgrader(cell)) {
      nbgrader_cell_selected = true;
      alert_move_cell_disabled();
    }
    return nbgrader_cell_selected;
  });
  return !nbgrader_cell_selected;
}

/**
 * Turn a cell to code if it is not a nbgrader cell,
 * otherwise display a warning
 */
function to_code() {
  if (utils.is_nbgrader(Jupyter.notebook.get_cell(arguments[0]))) {
    alert_cell_type_select_blocked();
  } else {
    old_to_code.apply(this, arguments);
  }
}

/**
 * Turn a cell to markdown if it is not a nbgrader cell,
 * otherwise display a warning
 */
function to_markdown() {
  if (utils.is_nbgrader(Jupyter.notebook.get_cell(arguments[0]))) {
    alert_cell_type_select_blocked();
  } else {
    old_to_markdown.apply(this, arguments);
  }
}

/**
 * Turn a cell to raw if it is not a nbgrader cell,
 * otherwise display a warning
 */
function to_raw() {
  if (utils.is_nbgrader(Jupyter.notebook.get_cell(arguments[0]))) {
    alert_cell_type_select_blocked();
  } else {
    old_to_raw.apply(this, arguments);
  }
}

/**
 * Move cell down if it is not a nbgrader cell,
 * otherwise display a warning
 */
function move_cell_down() {
  let index = arguments[0];
  if (index === undefined) {
    Jupyter.notebook.move_selection_down();
  } else if (validate_move_cells([Jupyter.notebook.get_cell(index)])) {
    old_move_cell_down.apply(this, arguments);
  }
}

/**
 * Move cell up if it is not a nbgrader cell,
 * otherwise display a warning
 */
function move_cell_up() {
  let index = arguments[0];
  if (index === undefined) {
    Jupyter.notebook.move_selection_down();
  } else if (validate_move_cells([Jupyter.notebook.get_cell(index)])) {
    old_move_cell_up.apply(this, arguments);
  }
}

/**
 * Move selection down if it does not contain a nbgrader cell,
 * otherwise display a warning
 */
function move_selection_down() {
  if (validate_move_cells(Jupyter.notebook.get_selected_cells())) {
    old_move_selection_down.apply(this, arguments);
  }
}

/**
 * Move selection up if it does not contain a nbgrader cell,
 * otherwise display a warning
 */
function move_selection_up() {
  if (validate_move_cells(Jupyter.notebook.get_selected_cells())) {
    old_move_selection_up.apply(this, arguments);
  }
}

/**
 * Paste and replace cells from clipboard,
 * remove all nbgrader cells
 */
function paste_cell_replace() {
  this.clipboard = sanitize_clipboard(this.clipboard);
  old_paste_cell_replace.apply(this, arguments);
}

/**
 * Paste cells above from clipboard,
 * remove all nbgrader cells
 */
function paste_cell_above() {
  this.clipboard = sanitize_clipboard(this.clipboard);
  old_paste_cell_above.apply(this, arguments);
}

/**
 * Paste cells below from clipboard,
 * remove all nbgrader cells
 */
function paste_cell_below() {
  this.clipboard = sanitize_clipboard(this.clipboard);
  old_paste_cell_below.apply(this, arguments);
}

/**
 * Hide all test cells and display line numbers for code cells
 */
function update_cells() {
  Jupyter.notebook.get_cells().forEach(function (cell) {
    if (utils.is_test(cell) && utils.is_empty(cell)) {
      cell.element.hide();
    } else if (cell.cell_type === "code") {
      cell.show_line_numbers(true);
    }
  });
}

/**
 * Update the notebook functionality to avoid students changing the
 * structure of an assignment
 */
export function patch_assignment_notebook() {
  // Remove copy paste shortcuts
  Jupyter.keyboard_manager.command_shortcuts.remove_shortcut("v");
  Jupyter.keyboard_manager.command_shortcuts.remove_shortcut("c");

  // Replace prototypes of notebook
  Notebook.prototype.to_code = to_code;
  Notebook.prototype.to_markdown = to_markdown;
  Notebook.prototype.to_raw = to_raw;
  Notebook.prototype.move_cell_down = move_cell_down;
  Notebook.prototype.move_selection_down = move_selection_down;
  Notebook.prototype.move_cell_up = move_cell_up;
  Notebook.prototype.move_selection_up = move_selection_up;
  Notebook.prototype.paste_cell_replace = paste_cell_replace;
  Notebook.prototype.paste_cell_above = paste_cell_above;
  Notebook.prototype.paste_cell_below = paste_cell_below;

  // Hide test cells and show line numbers
  Cell.options_default.cm_config.lineNumbers = true;
  update_cells();
}
