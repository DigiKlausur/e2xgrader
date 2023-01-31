import { utils } from "@e2xgrader/utils";
import { utils as e2xutils } from "@e2xgrader/cells";

function remove_metadata(cell) {
  utils.remove_nbgrader_metadata(cell);
  e2xutils.remove_e2x_metadata(cell);
}

function to_nbgrader(cell) {
  utils.create_nbgrader_metadata(cell);
  utils.set_schema_version(cell);
}

function to_manual_answer(cell) {
  to_nbgrader(cell);
  utils.set_solution(cell, true);
  utils.set_grade(cell, true);
  utils.set_locked(cell, false);
  utils.set_task(cell, false);
}

function to_autograded_answer(cell) {
  to_nbgrader(cell);
  utils.set_solution(cell, true);
  utils.set_grade(cell, false);
  utils.set_locked(cell, false);
  utils.set_task(cell, false);
}

function to_read_only(cell) {
  remove_metadata(cell);
  to_nbgrader(cell);
  utils.set_solution(cell, false);
  utils.set_grade(cell, false);
  utils.set_locked(cell, true);
  utils.set_task(cell, false);
}

function to_task(cell) {
  to_nbgrader(cell);
  utils.set_solution(cell, false);
  utils.set_grade(cell, false);
  utils.set_locked(cell, true);
  utils.set_task(cell, true);
}

function to_test(cell) {
  to_nbgrader(cell);
  utils.set_solution(cell, false);
  utils.set_grade(cell, true);
  utils.set_locked(cell, true);
  utils.set_task(cell, false);
}

function to_e2x_answer(cell, type) {
  to_manual_answer(cell);
  e2xutils.remove_e2x_metadata(cell);
  e2xutils.create_e2x_metadata(cell, type);
  cell.unrender_force();
  cell.render();
}

function to_pdf(cell) {
  to_read_only(cell);
  e2xutils.remove_e2x_metadata(cell);
  e2xutils.create_e2x_metadata(cell, "pdf");
  cell.unrender_force();
  cell.render();
}

export class CellFactory {
  constructor() {
    this.cell_types = {
      manual: to_manual_answer,
      task: to_task,
      singlechoice: (cell) => to_e2x_answer(cell, "singlechoice"),
      multiplechoice: (cell) => to_e2x_answer(cell, "multiplechoice"),
      attachments: (cell) => to_e2x_answer(cell, "attachments"),
      diagram: (cell) => to_e2x_answer(cell, "diagram"),
      pdf: to_pdf,
      readonly: to_read_only,
      tests: to_test,
      solution: to_autograded_answer,
      "": remove_metadata,
    };
  }

  to_cell(cell, cell_type) {
    if (this.cell_types.hasOwnProperty(cell_type)) {
      this.cell_types[cell_type](cell);
    } else {
      throw new Error("invalid nbgrader cell type: " + cell_type);
    }
  }

  get_type(cell) {
    if (e2xutils.is_e2x(cell)) {
      return e2xutils.get_e2x_cell_type(cell);
    } else if (utils.is_task(cell)) {
      return "task";
    } else if (utils.is_solution(cell) && utils.is_grade(cell)) {
      return "manual";
    } else if (utils.is_solution(cell) && cell.cell_type === "code") {
      return "solution";
    } else if (utils.is_grade(cell) && cell.cell_type === "code") {
      return "tests";
    } else if (utils.is_locked(cell)) {
      return "readonly";
    }
    return "";
  }
}
