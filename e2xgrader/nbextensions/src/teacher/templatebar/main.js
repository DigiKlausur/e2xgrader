define([
    'require',
    'jquery',
    'base/js/namespace',
    'notebook/js/celltoolbar',
    'base/js/events',
    './models/basemodel'
], function (require, $, Jupyter, nbcelltoolbar, events, model) {

    "use strict";

    var preset_name = 'Create Template';
    var CellToolbar = nbcelltoolbar.CellToolbar;

    CellToolbar.prototype.old_rebuild = CellToolbar.prototype.rebuild;
    CellToolbar.prototype.rebuild = function () {
        events.trigger('toolbar_rebuild.CellToolbar', this.cell);
        this.old_rebuild();
    }

    // remove nbgrader class when the cell is either hidden or rebuilt
    events.on("global_hide.CellToolbar toolbar_rebuild.CellToolbar", function (evt, cell) {
        if (cell.element && cell.element.hasClass('template_highlight')) {
            cell.element.removeClass('template_highlight');
        }
    });

    function load_css(file) {
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = require.toUrl('./' + file);
        document.getElementsByTagName("head")[0].appendChild(link);
    }

    function display_type(div, cell, celltoolbar) {
    	if (cell.cell_type === null) {
    		setTimeout(function () {
                display_type(div, cell, celltoolbar);
            }, 100);
    	} else {
    		let title = model.get_role(cell);
            if (title != '') {
                $(div).append($('<span/>').text(title).attr('id', 'template_type'));
                $(cell.element).addClass('template_highlight');
            } else {
                $(cell.element).removeClass('template_highlight');
            }
    		
    	}
    }

    var load_extension = function () {

        load_css("templatebar.css");

        CellToolbar.register_callback('templatecreator.role', display_type);

        var preset = [
            'templatecreator.role',
        ];

        CellToolbar.register_preset(preset_name, preset, Jupyter.notebook);

    };

    return {
        'load_ipython_extension': load_extension
    };
});