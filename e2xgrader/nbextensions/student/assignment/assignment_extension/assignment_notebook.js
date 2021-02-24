define([
    'jquery',
    'base/js/namespace',
    'base/js/dialog',
    'notebook/js/notebook',
    'notebook/js/cell',
    'notebook/js/textcell',
    'base/js/events',
    './model/nbgrader_model',
    './model/extracell'
], function ($, Jupyter, dialog, notebook, basecell, textcell, events, model, extramodel) {

    "use strict";

    let Notebook = notebook.Notebook;
    let MarkdownCell = textcell.MarkdownCell;

    function alert_move_cell_disabled() {
        let body = $('<div/>')
            .append($('<span/>')
                .text('At least one of the selected cells belongs to the assignment and can not be moved!'));
        dialog.modal({
            keyboard_manager: Jupyter.keyboard_manager,
            title: 'Can not move cells',
            body: body,
            buttons: {
                OK: {}
            }
        });
    }

    function alert_cell_type_select_blocked() {
        let body = $('<div/>')
            .append($('<span/>')
                .text('You can not change the type of a cell that belongs to the assignment!'));
        dialog.modal({
            keyboard_manager: Jupyter.keyboard_manager,
            title: 'Can not change cell type',
            body: body,
            buttons: {
                OK: {}
            }
        });
    }

    function patch_cell_type_select() {
        let old_to_code = Notebook.prototype.to_code;
        let old_to_markdown = Notebook.prototype.to_markdown;
        let old_to_raw = Notebook.prototype.to_raw;

        Notebook.prototype.to_code = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                alert_cell_type_select_blocked()
            } else {
                old_to_code.apply(this, arguments);
            }
        }

        Notebook.prototype.to_markdown = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                alert_cell_type_select_blocked()
            } else {
                old_to_markdown.apply(this, arguments);
            }
        }

        Notebook.prototype.to_raw = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                alert_cell_type_select_blocked()
            } else {
                old_to_raw.apply(this, arguments);
            }
        }
    }


    function patch_MarkdownCell_unrender() {
        let old_unrender = MarkdownCell.prototype.unrender;

        MarkdownCell.prototype.unrender = function () {
            if (!model.is_description_cell(this) || extramodel.is_pdf(cell)) {
                old_unrender.apply(this, arguments);
            }
        }
    }
    

    function patch_move_cells() {

        let old_move_cell_down = Notebook.prototype.move_cell_down;
        let old_move_selection_down = Notebook.prototype.move_selection_down;
        let old_move_cell_up = Notebook.prototype.move_cell_up;
        let old_move_selection_up = Notebook.prototype.move_selection_up;

        Notebook.prototype.move_cell_down = function () {
            let index = arguments[0];
            if (index === undefined) {
                Jupyter.notebook.move_selection_down();
            } else {
                let cell = Jupyter.notebook.get_cell(index);
                if (model.is_nbgrader_cell(cell)) {
                    alert_move_cell_disabled();
                } else {
                    old_move_cell_down.apply(this, arguments);
                }
            }            
        }

        Notebook.prototype.move_cell_up = function () {
            let index = arguments[0];
            if (index === undefined) {
                Jupyter.notebook.move_selection_up();
            } else {
                let cell = Jupyter.notebook.get_cell(index);
                if (model.is_nbgrader_cell(cell)) {
                    alert_move_cell_disabled();
                } else {
                    old_move_cell_up.apply(this, arguments);
                }
            }            
        }

        Notebook.prototype.move_selection_down = function () {
            let cells = Jupyter.notebook.get_selected_cells();
            let nbgrader_cell_selected = false;
            cells.some(function(cell) {
                let nbgrader_cell = model.is_nbgrader_cell(cell);
                if (nbgrader_cell) {
                    nbgrader_cell_selected = true;
                    alert_move_cell_disabled();
                }
                return nbgrader_cell;
            });
            if (!nbgrader_cell_selected) {
                old_move_selection_down.apply(this, arguments);
            }
        }

        Notebook.prototype.move_selection_up = function () {
            let cells = Jupyter.notebook.get_selected_cells();
            let nbgrader_cell_selected = false;
            cells.some(function(cell) {
                let nbgrader_cell = model.is_nbgrader_cell(cell);
                if (nbgrader_cell) {
                    nbgrader_cell_selected = true;
                    alert_move_cell_disabled();
                }
                return nbgrader_cell;
            });
            if (!nbgrader_cell_selected) {
                old_move_selection_up.apply(this, arguments);
            }
        }
    }


    function patch_paste_cell() {

        let old_paste_cell_replace = Notebook.prototype.paste_cell_replace;
        let old_paste_cell_above = Notebook.prototype.paste_cell_above;
        let old_paste_cell_below = Notebook.prototype.paste_cell_below;

        // Remove Ctrl-V command shortcut
        Jupyter.keyboard_manager.command_shortcuts.remove_shortcut('Cmdtrl-V');

        function sanitize_clipboard(clipboard) {
            if (clipboard === null) {
                return clipboard;
            }
            console.log('Clipboard:');
            console.log(clipboard);
            
            let sanitized = [];
            clipboard.forEach(function(cell) {
                if (!model.is_nbgrader_cell(cell)) {
                    sanitized.push(cell);
                }
            })
            console.log('Sanitized clipboard:');
            console.log(sanitized);
            if (sanitized.length == 0) {
                return null;
            }
            return sanitized;
        }

        Notebook.prototype.paste_cell_replace = function () {
            this.clipboard = sanitize_clipboard(this.clipboard);
            old_paste_cell_replace.apply(this, arguments);
        }

        Notebook.prototype.paste_cell_above = function () {
            this.clipboard = sanitize_clipboard(this.clipboard);
            old_paste_cell_above.apply(this, arguments);
        }

        Notebook.prototype.paste_cell_below = function () {
            this.clipboard = sanitize_clipboard(this.clipboard);
            old_paste_cell_below.apply(this, arguments);
        }

    }

    function update_cells() {
        Jupyter.notebook.get_cells().forEach(function (cell) {
            if (model.is_test_cell(cell) && model.is_empty_cell(cell)) {
                cell.element.hide();
            } else if (cell.cell_type === 'code') {
                cell.show_line_numbers(true);
            }
        })
    }

    function initialize() {        
        basecell.Cell.options_default.cm_config.lineNumbers = true;
        patch_cell_type_select();
        patch_MarkdownCell_unrender();
        patch_move_cells();
        patch_paste_cell();
        update_cells();
        console.log('Assignment notebook initialized!');
    }

    return {
        initialize: initialize
    }

});