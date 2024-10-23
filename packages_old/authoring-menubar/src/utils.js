import Jupyter from "base/js/namespace";
import { utils } from "@e2xgrader/utils";

function get_valid_name(name) {
  let alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let alphabet_lower = alphabet_upper.toLowerCase();
  let digits = "0123456789";
  let special = "_";
  let valid = alphabet_upper + alphabet_lower + digits + special;
  let invalid = "";
  for (let i = 0; i < name.length; i++) {
    if (valid.indexOf(name.charAt(i)) < 0) {
      invalid += name.charAt(i);
    }
  }

  for (let i = 0; i < invalid.length; i++) {
    name = name.replace(invalid.charAt(i), "_");
  }
  return name;
}

export function get_valid_task_name() {
  let ids = new Set();
  let nb_name = Jupyter.notebook.notebook_name.split(".ipynb")[0];
  // Validate the name
  nb_name = get_valid_name(nb_name);

  Jupyter.notebook.get_cells().forEach(function (cell) {
    if (utils.is_nbgrader(cell)) {
      ids.add(utils.get_grade_id(cell));
    }
  });
  let char = 65;
  let task_name = nb_name + "_" + String.fromCharCode(char);
  while (ids.has(task_name)) {
    char += 1;
    task_name = nb_name + "_" + String.fromCharCode(char);
  }
  return task_name;
}

export function set_task_ids(cells, task_name, points) {
  let n_read_only = 0;
  let n_tests = 0;
  cells.forEach((cell) => {
    if (utils.is_grade(cell)) {
      utils.set_points(cell, points);
    }
    if (utils.is_solution(cell)) {
      utils.set_grade_id(cell, task_name);
    } else if (utils.is_description(cell)) {
      utils.set_grade_id(cell, task_name + "_description" + n_read_only);
      n_read_only += 1;
    } else if (utils.is_test(cell)) {
      utils.set_grade_id(cell, "test" + n_tests + "_" + task_name);
      n_tests += 1;
    }
  });
}

export function set_template_ids(cells, template_name) {
  cells.forEach((cell, index) => {
    if (utils.is_nbgrader(cell)) {
      utils.set_grade_id(cell, template_name + "_" + index);
    }
  });
}

export function get_file_options() {
  let path = Jupyter.utils.url_path_join(
    Jupyter.notebook.base_url,
    "tree",
    Jupyter.notebook.notebook_path.replace(Jupyter.notebook.notebook_name, ""),
  );
  return [
    {
      label: "Images",
      callback: () => window.open(Jupyter.utils.url_path_join(path, "img")),
    },
    {
      label: "Other Files",
      callback: () => window.open(Jupyter.utils.url_path_join(path, "data")),
    },
  ];
}

export function insert_cells(cells) {
  let idx = Jupyter.notebook.ncells();
  cells.forEach((cell) => {
    let new_cell = Jupyter.notebook.insert_cell_at_index(cell.cell_type, idx);
    new_cell.set_text(cell.source);
    if (cell.metadata !== undefined) {
      new_cell.metadata = cell.metadata;
    }
    idx += 1;
  });
}
