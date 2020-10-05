define([
    'jquery',
    'require',
    'base/js/namespace',
    'base/js/events',
    'notebook/js/textcell',
    './extended_cell/extended_cell',
    './extended_cell/choice_cell'
], function (
    $,
    require,
    Jupyter,
    events,
    textcell,
    extended_cell,
    choice_cell,
) {

    'use strict';

    var MarkdownCell = textcell.MarkdownCell;
    var old_render = MarkdownCell.prototype.render;
    var old_unrender = MarkdownCell.prototype.unrender;
    var edit_mode = false;

    function cell_type (cell) {
        if (cell.metadata.hasOwnProperty('extended_cell')) {
            return cell.metadata.extended_cell.type;
        }
        return cell.cell_type;
    };

    function patch_MarkdownCell_render () {
        MarkdownCell.prototype.render_force = old_render;
        MarkdownCell.prototype.render = function () {
            var type = cell_type(this);
            if (type == 'singlechoice') {
                var sc = new choice_cell.SinglechoiceCell(this);
                sc.edit_mode = edit_mode;
                sc.render();
            } else if (type == 'multiplechoice') {
                var mc = new choice_cell.MultiplechoiceCell(this);
                mc.edit_mode = edit_mode;
                mc.render();
            } else {
                old_render.apply(this, arguments);
            }
        }
    };

    function patch_MarkdownCell_unrender () {
        MarkdownCell.prototype.unrender_force = old_unrender;
        MarkdownCell.prototype.unrender = function () {
            var type = cell_type(this);
            if (type == 'singlechoice') {
                
            } else if (type == 'multiplechoice') {

            } else {
                old_unrender.apply(this, arguments);
            }
        }
    };

    function render_extended_cells () {
        var cells = Jupyter.notebook.get_cells();
        for (var i in cells) {
            var cell = cells[i];
            if (cell.metadata.hasOwnProperty('extended_cell') && cell.rendered) {
                cell.unrender_force();
                cell.render();
            }
        }
    };
    
    function load_css () {
        var link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./extra_cells.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    };

    function initialize () {
        load_css();
        if (Jupyter.notebook.metadata.hasOwnProperty('celltoolbar')) {
            if (Jupyter.notebook.metadata.celltoolbar == 'Create Assignment') {
                edit_mode = true;
            }
        }
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
    };

    var load_ipython_extension = function () {
        return Jupyter.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };

});
