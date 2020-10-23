define([
    'base/js/namespace'
], function(
    Jupyter
) {
    "use strict";

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

    let is_init_cell = function (cell) {
        if (cell.metadata.run_control === undefined) {
            return false;
        }
        return (cell.cell_type === 'code' && cell.metadata.run_control.init_cell);
    }

    let is_hidden_input_cell = function (cell) {
        if (cell.metadata.run_control === undefined) {
            return false;
        }
        return (cell.metadata.run_control.hide_input);
    }

    let is_hidden_cell = function (cell) {
        if (cell.metadata.run_control === undefined) {
            return false;
        }
        return (cell.metadata.run_control.hide_cell);
    }

    let is_frozen_cell = function (cell) {
        if (cell.metadata.run_control === undefined) {
            return false;
        }
        return (cell.metadata.run_control.frozen);
    }

    let is_multiple_choice_cell = function (cell) {
        if (cell.metadata.egrader === undefined) {
            return false;
        }
        return (cell.metadata.egrader.type === 'multiple_choice' &&
                cell.cell_type === 'markdown');
    }

    let load_css = function(name) {
        let link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = require.toUrl("./" + name);
        document.getElementsByTagName("head")[0].appendChild(link);
    };


    let get_cell_by_id = function (id) {
        let cells = Jupyter.notebook.get_cells();
        for (let i in cells) {
            let cell = cells[i];
            if (cell.metadata.cell_id === id) {
                return cell;
            }
        }
        return null;
    }


    let utils = {
        is_init_cell: is_init_cell,
        is_hidden_input_cell: is_hidden_input_cell,
        is_hidden_cell: is_hidden_cell,
        is_frozen_cell: is_frozen_cell,
        is_multiple_choice_cell: is_multiple_choice_cell,
        load_css: load_css,
        get_cell_by_id: get_cell_by_id,
        is_test_cell: is_test_cell,
        is_description_cell: is_description_cell
    }

    return utils;
});