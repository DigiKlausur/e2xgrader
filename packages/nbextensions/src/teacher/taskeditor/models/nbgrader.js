define([], function () {
  "use strict";

  class NbgraderModel {
    is_nbgrader(cell) {
      return (
        cell.hasOwnProperty("metadata") &&
        cell.metadata.hasOwnProperty("nbgrader")
      );
    }

    is_locked(cell) {
      return this.is_nbgrader(cell) && cell.metadata.nbgrader.locked;
    }

    is_solution(cell) {
      return this.is_nbgrader(cell) && cell.metadata.nbgrader.solution;
    }

    is_grade(cell) {
      return this.is_nbgrader(cell) && cell.metadata.nbgrader.grade;
    }

    is_description(cell) {
      return this.is_locked(cell) && !this.is_grade(cell);
    }

    to_description(cell, id) {
      if (this.is_nbgrader(cell)) {
        delete cell.metadata.nbgrader;
      }
      cell.metadata.nbgrader = {
        locked: true,
        grade: false,
        solution: false,
        task: false,
        grade_id: id,
        schema_version: 3,
      };
    }

    is_test(cell) {
      return this.is_locked(cell) && this.is_grade(cell);
    }

    set_id(cell, id) {
      if (this.is_nbgrader(cell)) {
        cell.metadata.nbgrader.grade_id = id;
      }
    }

    get_id(cell) {
      if (this.is_nbgrader(cell)) {
        return cell.metadata.nbgrader.grade_id;
      }
      return "";
    }

    set_points(cell, points) {
      if (this.is_nbgrader(cell)) {
        cell.metadata.nbgrader.points = points;
      }
    }
  }

  return {
    NbgraderModel: NbgraderModel,
  };
});
