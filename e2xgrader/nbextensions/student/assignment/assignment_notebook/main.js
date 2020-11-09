define([
    'require',
    'jquery',
    'base/js/namespace',
    'notebook/js/notebook',
    'notebook/js/cell',
    'notebook/js/textcell',
    'base/js/events',
    './model/nbgrader_model'
], function (require, $, Jupyter, notebook, basecell, textcell, events, model) {

    let Notebook = notebook.Notebook;
    let MarkdownCell = textcell.MarkdownCell;

    function patch_cell_type_select(func) {
        let old_to_code = Notebook.prototype.to_code;
        let old_to_markdown = Notebook.prototype.to_markdown;
        let old_to_raw = Notebook.prototype.to_raw;

        Notebook.prototype.to_code = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                console.log('Can not change cell type of nbgrader cells');
            } else {
                old_to_code.apply(this, arguments);
            }
        }

        Notebook.prototype.to_markdown = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                console.log('Can not change cell type of nbgrader cells');
            } else {
                old_to_markdown.apply(this, arguments);
            }
        }

        Notebook.prototype.to_raw = function () {
            let cell = Jupyter.notebook.get_cell(arguments[0]);
            if (model.is_nbgrader_cell(cell)) {
                console.log('Can not change cell type of nbgrader cells');
            } else {
                old_to_raw.apply(this, arguments);
            }
        }
    }

    function patch_MarkdownCell_unrender() {
        let old_unrender = MarkdownCell.prototype.unrender;

        MarkdownCell.prototype.unrender = function () {
            if (!model.is_description_cell(this)) {
                old_unrender.apply(this, arguments);
            }
        }
    }

    function update_cells() {
        Jupyter.notebook.get_cells().forEach(function (cell) {
            if (model.is_test_cell(cell)) {
                cell.element.hide();
            } else if (cell.cell_type === 'code') {
                cell.show_line_numbers(true);
            }
        })
    }

    function init() {
        console.log('Assignment notebook initialized!');
        basecell.Cell.options_default.cm_config.lineNumbers = true;
        patch_cell_type_select();
        patch_MarkdownCell_unrender();
        update_cells();
    }


    function load_extension() {
        if (Jupyter.notebook) {
            init();
        } else {
            events.on('notebook_loaded.notebook', () => init());
        }
    }

    return {
        load_ipython_extension: load_extension
    }

});