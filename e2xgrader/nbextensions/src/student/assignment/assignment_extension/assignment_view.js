define([
    'require',
    'jquery',
    'base/js/namespace',
    'notebook/js/celltoolbar',
    'base/js/events',
], function (require, $, Jupyter, nbcelltoolbar, events) {

    "use strict";

    let model = undefined;
    let preset_name = "Assignment View";
    let CellToolbar = nbcelltoolbar.CellToolbar;
    let highlight = 'highlight';
    let minimized = 'minimized';

    events.on("global_hide.CellToolbar toolbar_rebuild.CellToolbar", function (evt, cell) {
        if (cell.celltoolbar === null) {
            return;
        }
        if (cell.celltoolbar.inner_element.hasClass(highlight)) {
            cell.celltoolbar.inner_element.removeClass(highlight);
        } else if (cell.celltoolbar.inner_element.hasClass(minimized)) {
            cell.celltoolbar.inner_element.removeClass(minimized);
        }
    });

    function add_highlight(cell) {
        if (cell.celltoolbar !== undefined) {
            if (!cell.celltoolbar.inner_element.hasClass(highlight)) {
                cell.celltoolbar.inner_element.addClass(highlight);
            }
        }
    }

    function add_hidden(cell) {
        if (cell.celltoolbar !== undefined) {
            if (!cell.celltoolbar.inner_element.hasClass(minimized)) {
                cell.celltoolbar.inner_element.addClass(minimized);
            }
        }
    }

    function remove_classes(cell) {
        if (cell.celltoolbar !== null && cell.celltoolbar !== undefined) {
            if (cell.celltoolbar.inner_element.hasClass(highlight)) {
                cell.celltoolbar.inner_element.removeClass(highlight);
            } else if (cell.celltoolbar.inner_element.hasClass(minimized)) {
                cell.celltoolbar.inner_element.removeClass(minimized);
            }
        }
    }

    function create_button(btn_text, btn_id, callback) {
        let btn = $('<button/>').attr('type', 'button').attr('id', btn_id)
                    .addClass('exam_btn').text(btn_text);
        btn.click(callback);
        return btn;
    }

    function create_header(div, cell, celltoolbar) {
        if (cell.cell_type === null) {
            setTimeout(function () {
                create_header(div, cell, celltoolbar);
            }, 100);
        } else {
            if (!model.is_solution_cell(cell)) {
                remove_classes(cell);
                add_hidden(cell);
                return;
            }
            add_highlight(cell);
            if (model.is_extra_cell(cell)) {
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
    }

    /**
     * Load custom css for the nbgrader toolbar.
     */
    function load_css() {
        let link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./assignment_view.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    }

    function initialize() {
        load_css();
        let static_path = Jupyter.notebook.base_url + 'e2xbase/static/js/models/';
        require([static_path + 'nbgrader.js'], function(nbgrader) {
            
            model = nbgrader;

            CellToolbar.register_callback('assignment_view.create_header', create_header);
            let preset = [
                'assignment_view.create_header',
            ];
            CellToolbar.register_preset(preset_name, preset, Jupyter.notebook);

            // Activate the toolbar
            CellToolbar.activate_preset(preset_name);
            Jupyter.CellToolbar.global_show();
        });
    }

    return {
        initialize: initialize
    };
    
});