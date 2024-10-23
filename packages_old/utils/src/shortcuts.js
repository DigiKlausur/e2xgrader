import Jupyter from "base/js/namespace";
import { Notebook } from "notebook/js/notebook";

/**
 * Defines a new method `execute_cell_and_select_below_without_insert()` for the `Notebook` prototype object,
 * which executes the currently selected cell and then selects the cell below it.
 */
function add_Notebook_execute_cell_and_select() {
  Notebook.prototype.execute_cell_and_select_below_without_insert =
    function () {
      let indices = this.get_selected_cells_indices();
      let cell_index;
      if (indices.length > 1) {
        this.execute_cells(indices);
        cell_index = Math.max(...indices);
      } else {
        let cell = this.get_selected_cell();
        cell_index = this.find_cell_index(cell);
        cell.execute();
      }

      // If we are at the end do not insert a new cell
      cell_index = Math.min(cell_index + 1, this.ncells() - 1);
      this.select(cell_index);
      this.focus_cell();
    };
}

/**
 * Returns the keyboard manager object for the specified mode.
 * @param {string} mode - The keyboard manager mode to get ("command" or "edit").
 * @throws {Error} If the mode is not "command" or "edit".
 * @returns {object} The keyboard manager object for the specified mode.
 */
function get_manager(mode) {
  if (mode === "command") {
    return Jupyter.keyboard_manager.command_shortcuts;
  } else if (mode === "edit") {
    return Jupyter.keyboard_manager.edit_shortcuts;
  } else {
    throw new Error("Mode needs to be either 'command' or 'edit'");
  }
}

/**
 * Removes the specified shortcuts from the keyboard manager for the specified mode.
 * @param {string} mode - The keyboard manager mode to remove shortcuts from ("command" or "edit").
 * @param  {...string} shortcuts - The shortcut keys to remove.
 */
export function remove_shortcuts(mode, ...shortcuts) {
  const manager = get_manager(mode);
  for (const shortcut of shortcuts) {
    try {
      manager.remove_shortcut(shortcut);
    } catch (e) {
      console.log(
        "Error removing shortcut",
        shortcut,
        "from",
        mode,
        "mode:",
        e.message,
      );
      // Shortcut does not exist and can't be removed;
    }
  }
}

/**
 * Adds a new shortcut to the keyboard manager for the specified mode.
 * @param {string} mode - The keyboard manager mode to add the shortcut to ("command" or "edit").
 * @param {string} key - The key combination for the shortcut.
 * @param {function} handler - The function to be called when the shortcut is activated.
 * @param {string} help - The help text for the shortcut.
 * @param {string} [help_index="zz"] - The help index for the shortcut.
 */
export function add_shortcut(mode, key, handler, help, help_index = "zz") {
  const manager = get_manager(mode);
  manager.add_shortcut(key, {
    help: help,
    help_index: help_index,
    handler: handler,
  });
}

/**
 * Disables the default behavior of adding a new cell after executing a cell by removing the "alt-enter" and "shift-enter"
 * shortcuts for both the command and edit modes, and adding new shortcuts that execute the current cell and select
 * the cell below it using the `execute_cell_and_select_below_without_insert()` method.
 */
export function disable_add_cell_on_execute() {
  add_Notebook_execute_cell_and_select();
  const shortcut_keys = ["alt-enter", "shift-enter"];
  remove_shortcuts("edit", ...shortcut_keys);
  remove_shortcuts("command", ...shortcut_keys);

  const help = "run cell";
  const handler = function (event) {
    Jupyter.notebook.execute_cell_and_select_below_without_insert();
    return false;
  };

  for (const key of shortcut_keys) {
    add_shortcut("edit", key, handler, help);
    add_shortcut("command", key, handler, help);
  }
}
