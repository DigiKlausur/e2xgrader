define([
], function () {

    'use strict';

    var nbgrader_schema_version = 3;

    var to_float = function(val) {
        if (val === undefined || val === "") {
            return 0;
        }
        return parseFloat(val);
    };

    var randomString = function(length) {
        var result = '';
        var chars = 'abcdef0123456789';
        var i;
        for (i=0; i < length; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return result;
    };

    /**
     * Remove all nbgrader metadata
     */
    var remove_metadata = function (cell) {
        if (cell.metadata.hasOwnProperty("nbgrader")) {
            delete cell.metadata.nbgrader;
        }
    };

    /**
     * Set nbgrader schema version
     */
    var set_schema_version = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.schema_version = nbgrader_schema_version;
    };

    /**
     * Get nbgrader schema version
     */
    var get_schema_version = function (cell) {
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
    var is_solution = function (cell) {
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
    var set_solution = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.solution = val;
    };

    /**
     * Is the cell a grade cell?
     */
    var is_grade = function (cell) {
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
    var set_grade = function (cell, val) {
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
    var is_task = function (cell) {
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
    var set_task = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        cell.metadata.nbgrader.task = val;
    };

    var is_graded = function (cell) {
        return ( is_grade(cell) || is_task(cell) );
    };


    var get_points = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return 0;
        } else {
            return to_float(cell.metadata.nbgrader.points);
        }
    };

    var set_points = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        var points = to_float(val);
        if (points < 0) points = 0;
        cell.metadata.nbgrader.points = points;
    };

    var get_grade_id = function (cell) {
        if (cell.metadata.nbgrader === undefined) {
            return "cell-" + randomString(16);
        } else if (cell.metadata.nbgrader.grade_id === undefined) {
            return "cell-" + randomString(16);
        } else {
            return cell.metadata.nbgrader.grade_id;
        }
    };

    var set_grade_id = function (cell, val) {
        if (cell.metadata.nbgrader === undefined) {
            cell.metadata.nbgrader = {};
        }
        if (val === undefined) {
            cell.metadata.nbgrader.grade_id = '';
        } else {
            cell.metadata.nbgrader.grade_id = val;
        }
    };

    var is_locked = function (cell) {
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

    var set_locked = function (cell, val) {
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

    var is_invalid = function (cell) {
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
        is_invalid: is_invalid
    };
    
});