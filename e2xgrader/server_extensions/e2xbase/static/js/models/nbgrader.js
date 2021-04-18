define([
], function () {

    'use strict';

    let nbgrader_schema_version = 3;

    let to_float = function(val) {
        if (val === undefined || val === "") {
            return 0;
        }
        return parseFloat(val);
    };

    let randomString = function(length) {
        let result = '';
        let chars = 'abcdef0123456789';
        let i;
        for (i=0; i < length; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return result;
    };

    /**
     * Remove all nbgrader metadata
     */
    let remove_metadata = function (cell) {
        if (cell.metadata.hasOwnProperty("nbgrader")) {
            delete cell.metadata.nbgrader;
        }
    };

    /**
     * Set nbgrader schema version
     */
    let set_schema_version = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.schema_version = nbgrader_schema_version;
    };

    /**
     * Get nbgrader schema version
     */
    let get_schema_version = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return undefined;
        }
        if (!cell.metadata.nbgrader.hasOwnProperty("schema_version")) {
            return 0;
        }
        return cell.metadata.nbgrader.schema_version;
    };

    /**
     * Is the cell a solution cell?
     */
    let is_solution = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return false;
        } else if (cell.metadata.nbgrader.solution === undefined) {
            return false;
        } else {
            return cell.metadata.nbgrader.solution;
        }
    };

    /**
     * Set whether this cell is or is not a solution cell.
     */
    let set_solution = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.solution = val;
    };

    /**
     * Is the cell a grade cell?
     */
    let is_grade = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return false;
        } else if (cell.metadata.nbgrader.grade === undefined) {
            return false;
        } else {
            return cell.metadata.nbgrader.grade;
        }
    };

    /**
     * Set whether this cell is or is not a grade cell.
     */
    let set_grade = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.grade = val;
        if (val === false && cell.metadata.nbgrader.hasOwnProperty("points")) {
            delete cell.metadata.nbgrader.points;
        }
    };

    /**
     * Is the cell a task cell?
     */
    let is_task = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return false;
        } else if (cell.metadata.nbgrader.task === undefined) {
            return false;
        } else {
            return cell.metadata.nbgrader.task;
        }
    };

    /**
     * Set whether this cell is or is not a grade cell.
     */
    let set_task = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.task = val;
    };

    let is_graded = function (cell) {
        return ( is_grade(cell) || is_task(cell) );
    };


    let get_points = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return 0;
        } else {
            return to_float(cell.metadata.nbgrader.points);
        }
    };

    let set_points = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        let points = to_float(val);
        if (points < 0) points = 0;
        cell.metadata.nbgrader.points = points;
    };

    let get_grade_id = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return "cell-" + randomString(16);
        } else if (cell.metadata.nbgrader.grade_id === undefined) {
            return "cell-" + randomString(16);
        } else {
            return cell.metadata.nbgrader.grade_id;
        }
    };

    let set_grade_id = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        if (val === undefined) {
            cell.metadata.nbgrader.grade_id = '';
        } else {
            cell.metadata.nbgrader.grade_id = val;
        }
    };

    let is_locked = function (cell) {
        if (is_solution(cell)) {
            return false;
        } else if (is_graded(cell)) {
            return true;
        } else if (cell.metadata.nbgrader === undefined) {
            return false;
        } else if (cell.metadata.nbgrader.locked === undefined) {
            return false;
        } else {
            return cell.metadata.nbgrader.locked;
        }
    };

    let set_locked = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        if (is_solution(cell)) {
            cell.metadata.nbgrader.locked = false;
        } else if (is_graded(cell)) {
            cell.metadata.nbgrader.locked = true;
        } else {
            cell.metadata.nbgrader.locked = val;
        }
    };

    let is_invalid = function (cell) {
        if (is_task(cell)) {
            return false;
        } else if (is_solution(cell) && is_grade(cell)) {
            return false;
        } else if (is_solution(cell) && cell.cell_type !== "code") {
            return true;
        } else if (is_grade(cell) && cell.cell_type !== "code") {
            return true;
        } else {
            return false;
        }
    };

    function is_test_cell(cell) {
        return is_nbgrader_cell(cell) && 
               cell.metadata.nbgrader.locked && 
               cell.metadata.nbgrader.grade && 
               !cell.metadata.nbgrader.solution;
    }

    function is_description_cell(cell) {
        return is_nbgrader_cell(cell) &&
               cell.metadata.nbgrader.locked &&
               !cell.metadata.nbgrader.grade &&
               !cell.metadata.nbgrader.solution;
    }

    function is_nbgrader_cell(cell) {
        return cell.metadata.hasOwnProperty('nbgrader');
    }

    function is_empty_cell(cell) {
        return cell.code_mirror.getValue().length == 0
    }

    function is_solution_cell(cell) {
        return is_nbgrader_cell(cell) && cell.metadata.nbgrader.solution;
    }

    function is_extra_cell(cell){
        return is_solution_cell(cell) && cell.metadata.hasOwnProperty('extended_cell');
    }

    function is_assignment_notebook() {
        let is_nbgrader = false;
        Jupyter.notebook.get_cells().some(function (cell) {
            is_nbgrader = is_nbgrader_cell(cell);
            return is_nbgrader;
        });
        return is_nbgrader;
    }

    return {
        remove_metadata: remove_metadata,
        set_schema_version: set_schema_version,
        get_schema_version: get_schema_version,
        is_solution: is_solution,
        set_solution: set_solution,
        is_grade: is_grade,
        set_grade: set_grade,
        is_task: is_task,
        set_task: set_task,
        is_graded: is_graded,
        get_points: get_points,
        set_points: set_points,
        get_grade_id: get_grade_id,
        set_grade_id: set_grade_id,
        is_locked: is_locked,
        set_locked: set_locked,
        is_invalid: is_invalid,
        is_test_cell: is_test_cell,
        is_nbgrader_cell: is_nbgrader_cell,
        is_description_cell: is_description_cell,
        is_empty_cell: is_empty_cell,
        is_solution_cell: is_solution_cell,
        is_extra_cell: is_extra_cell,
        is_assignment_notebook: is_assignment_notebook
    };
    
});