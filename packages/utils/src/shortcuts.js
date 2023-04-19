import Jupyter from "base/js/namespace";
import { Notebook } from "notebook/js/notebook";

function add_Notebook_execute_cell_and_select() {
  Notebook.prototype.execute_cell_and_select_below_without_insert =
    function () {
      let indices = this.get_selected_cells_indices();
      let cell_index;
      if (indices.length > 1) {
        this.execute_cells(indices);
        cell_index = Math.max.apply(Math, indices);
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

function get_manager(mode) {
  if (mode === "command") {
    return Jupyter.keyboard_manager.command_shortcuts;
  } else if (mode === "edit") {
    return Jupyter.keyboard_manager.edit_shortcuts;
  } else {
    throw new Error("Mode needs to be either 'command' or 'edit'");
  }
}

export function remove_shortcuts(mode, ...shortcuts) {
  const manager = get_manager(mode);
  for (const shortcut of shortcuts) {
    try {
      manager.remove_shortcut(shortcut);
    } catch (e) {
      // Shortcut does not exist and can't be removed;
    }
  }
}

export function add_shortcut(mode, key, handler, help, help_index = "zz") {
  const manager = get_manager(mode);
  manager.add_shortcut(key, {
    help: help,
    help_index: help_index,
    handler: handler,
  });
}

export function disable_add_cell_on_execute() {
  add_Notebook_execute_cell_and_select();
  const shortcut_keys = ["alt-enter", "shift-enter"];
  remove_shortcuts("edit", shortcut_keys);
  remove_shortcuts("command", shortcut_keys);

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
