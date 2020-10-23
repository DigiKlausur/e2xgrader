define([
    'require',
    'jquery',
    'base/js/namespace',
    'base/js/dialog',
    'notebook/js/celltoolbar',
    'base/js/events',
    'notebook/js/codecell'

], function (require, $, Jupyter, dialog, nbcelltoolbar, events, codecell) {
    "use strict";

    let preset_name = "Assignment View";
    let CellToolbar = nbcelltoolbar.CellToolbar;
    let highlight = 'highlight';
    let minimized = 'minimized';

    events.on("global_hide.CellToolbar toolbar_rebuild.CellToolbar", function (evt, cell) {
        if (cell.celltoolbar.inner_element.hasClass(highlight)) {
            cell.celltoolbar.inner_element.removeClass(highlight);
        } else if (cell.celltoolbar.inner_element.hasClass(minimized)) {
            cell.celltoolbar.inner_element.removeClass(minimized);
        }
    });

    let is_nbgrader_cell = function(cell) {
        return (cell.metadata.hasOwnProperty('nbgrader'));
    };

    let is_solution_cell = function(cell) {
        return is_nbgrader_cell(cell) && cell.metadata.nbgrader.solution;
    };

    let is_extra_cell = function(cell) {
        return is_solution_cell(cell) && cell.metadata.hasOwnProperty('extended_cell');
    };

    let add_highlight = function(cell) {
        if (cell.celltoolbar !== undefined) {
            if (!cell.celltoolbar.inner_element.hasClass(highlight)) {
                cell.celltoolbar.inner_element.addClass(highlight);
            }
        }
    };

    let add_hidden = function(cell) {
        if (cell.celltoolbar !== undefined) {
            if (!cell.celltoolbar.inner_element.hasClass(minimized)) {
                cell.celltoolbar.inner_element.addClass(minimized);
            }
        }
    };

    let remove_classes = function(cell) {
        if (cell.celltoolbar !== null && cell.celltoolbar !== undefined) {
            if (cell.celltoolbar.inner_element.hasClass(highlight)) {
                cell.celltoolbar.inner_element.removeClass(highlight);
            } else if (cell.celltoolbar.inner_element.hasClass(minimized)) {
                cell.celltoolbar.inner_element.removeClass(minimized);
            }
        }
    };

    let create_button = function(btn_text, btn_id, callback) {
        let btn = $('<button/>').attr('type', 'button').attr('id', btn_id)
                    .addClass('exam_btn').text(btn_text);
        btn.click(callback);
        return btn;
    };

    let create_header = function(div, cell, celltoolbar) {
        if (cell.cell_type === null) {
            setTimeout(function () {
                create_run_button(div, cell, celltoolbar);
            }, 100);
        } else {
            if (!is_solution_cell(cell)) {
                remove_classes(cell);
                add_hidden(cell);
                return;
            }
            add_highlight(cell);
            if (is_extra_cell(cell)) {
                return;
            }
            if (cell.cell_type === 'code') {
                let btn = create_button('Run', 'run', function() {
                    cell.execute();
                });
                $(div).append($('<span/>').append(btn).addClass('cell_control'));
            } else if (cell.cell_type === 'markdown') {
                let edit_btn = create_button('Edit', 'edit', function() {
                        cell.events.trigger('select.Cell', {'cell': cell});
                        Jupyter.notebook.edit_mode();
                        celltoolbar.rebuild();
                    });
                let btn = create_button('Preview', 'preview', function() {
                    cell.execute();
                    celltoolbar.rebuild();
                });
                $(div).append($('<span/>').append(edit_btn).append(btn).addClass('cell_control'));
            }
        }
    };

    /**
     * Load custom css for the nbgrader toolbar.
     */
    let load_css = function () {
        let link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./assignment_view.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    };

    let initialize = function () {
        load_css();
        CellToolbar.register_callback('assignment_view.create_header', create_header);
        


        let preset = [
            'assignment_view.create_header',
        ];
        CellToolbar.register_preset(preset_name, preset, Jupyter.notebook);
        CellToolbar.activate_preset(preset_name);
        Jupyter.CellToolbar.global_show();
    }

    let load_ipython_extension = function () {
        return Jupyter.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };
    
});