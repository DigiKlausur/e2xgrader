define([
    'jquery',
    'require',
    'base/js/namespace',
    'base/js/events',
    'notebook/js/textcell',
    './extended_cell/extended_cell',
    './extended_cell/choice_cell',
    './extended_cell/attachment_cell'
], function (
    $,
    require,
    Jupyter,
    events,
    textcell,
    extended_cell,
    choice_cell,
    attachment_cell,
) {

    'use strict';

    let MarkdownCell = textcell.MarkdownCell;
    let TextCell = textcell.TextCell;
    let old_render = MarkdownCell.prototype.render;
    let old_unrender = MarkdownCell.prototype.unrender;
    let old_toJSON = TextCell.prototype.toJSON;
    let edit_mode = false;

    function cell_type (cell) {
        if (cell.metadata.hasOwnProperty('extended_cell')) {
            return cell.metadata.extended_cell.type;
        }
        return cell.cell_type;
    }

    function patch_TextCell_toJSON() {
        TextCell.prototype.toJSON = function () {
            let type = cell_type(this);
            if (type == 'attachments') {
                // Do not remove ununsed attachments
                arguments[0] = false;
                return old_toJSON.apply(this, arguments);
            } else {                
                return old_toJSON.apply(this, arguments);
            }
        }
    }

    function patch_MarkdownCell_render () {
        MarkdownCell.prototype.render_force = old_render;
        MarkdownCell.prototype.render = function () {
            let type = cell_type(this);
            if (type == 'singlechoice') {
                let sc = new choice_cell.SinglechoiceCell(this);
                sc.edit_mode = edit_mode;
                sc.render();
            } else if (type == 'multiplechoice') {
                let mc = new choice_cell.MultiplechoiceCell(this);
                mc.edit_mode = edit_mode;
                mc.render();
            } else if (type == 'attachments') {
                //console.log('AttachmentCell found!');
                let mycell = new attachment_cell.AttachmentCell(this);
                mycell.edit_mode = edit_mode;
                mycell.render();
                //let ac = new attachment_cell.AttachmentCell(this);
                //ac.render();
            } else {
                old_render.apply(this, arguments);
            }
        }
    }

    function patch_MarkdownCell_unrender () {
        MarkdownCell.prototype.unrender_force = old_unrender;
        MarkdownCell.prototype.unrender = function () {
            let type = cell_type(this);
            if (type != 'singlechoice' && type != 'multiplechoice' && type != 'attachments') {
                old_unrender.apply(this, arguments);
            }
        }
    }

    function render_extended_cells () {
        let cells = Jupyter.notebook.get_cells();
        for (let i in cells) {
            let cell = cells[i];
            if (cell.metadata.hasOwnProperty('extended_cell') && cell.rendered) {
                cell.unrender_force();
                cell.render();
            }
        }
    }
    
    function load_css () {
        let link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./extra_cells.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    }

    function initialize () {
        load_css();
        if (Jupyter.notebook.metadata.hasOwnProperty('celltoolbar')) {
            if (Jupyter.notebook.metadata.celltoolbar == 'Create Assignment') {
                edit_mode = true;
            }
        }
        patch_TextCell_toJSON();
        patch_MarkdownCell_render();
        patch_MarkdownCell_unrender();
        render_extended_cells();
        events.on('preset_activated.CellToolbar', function (evt, preset) {
            console.log('Preset changed to '+preset.name);
            if (preset.name == 'Create Assignment') {
                edit_mode = true;
            } else {
                edit_mode = false;
            }
            render_extended_cells();
        });
        events.on('global_hide.CellToolbar', function (evt, instance) {
            edit_mode = false;
            render_extended_cells();
        })
    }

    let load_ipython_extension = function () {
        return Jupyter.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };

});
