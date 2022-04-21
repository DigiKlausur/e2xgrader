define([
    'require',
    'jquery',
    'base/js/namespace',
    'base/js/dialog',
    'notebook/js/celltoolbar',
    'base/js/events',
], function (require, $, Jupyter, dialog, toolbar, events) {

    "use strict";

    let model = undefined;
    let extramodel = undefined;
    var nbgrader_preset_name = "Create Assignment";
    var nbgrader_highlight_cls = "nbgrader-highlight";
    var nbgrader_cls = "nbgrader-cell";
    var nbgrader_schema_version = 3;
    var warning;

    var CellToolbar = toolbar.CellToolbar;

    // trigger an event when the toolbar is being rebuilt
    CellToolbar.prototype._rebuild = CellToolbar.prototype.rebuild;
    CellToolbar.prototype.rebuild = function () {
        events.trigger('toolbar_rebuild.CellToolbar', this.cell);
        this._rebuild();
    };

    // trigger an event when the toolbar is being (globally) hidden
    CellToolbar._global_hide = CellToolbar.global_hide;
    CellToolbar.global_hide = function () {
        $("#nbgrader-total-points-group").hide();

        CellToolbar._global_hide();
        for (let instance of CellToolbar._instances) {
            events.trigger('global_hide.CellToolbar', instance.cell);
        }
    };

    // show the total points when the preset is activated
    events.on('preset_activated.CellToolbar', function(evt, preset) {
        validate_schema_version();
        clear_cell_types();

        var elem = $("#nbgrader-total-points-group");
        if (preset.name === nbgrader_preset_name) {
            if (elem.length == 0) {
                elem = $("<div />").attr("id", "nbgrader-total-points-group");
                elem.addClass("btn-group");
                elem.append($("<span />").text("Total points:"));
                elem.append($("<input />")
                            .attr("disabled", "disabled")
                            .attr("type", "number")
                            .attr("id", "nbgrader-total-points"));
                $("#maintoolbar-container").append(elem);
            }
            elem.show();
            update_total();
        } else {
            elem.hide();
        }
    });

    // remove nbgrader class when the cell is either hidden or rebuilt
    events.on("global_hide.CellToolbar toolbar_rebuild.CellToolbar", function (evt, cell) {
        if (cell.element && cell.element.hasClass(nbgrader_cls)) {
            cell.element.removeClass(nbgrader_cls);
        }
        if (cell.element && cell.element.hasClass(nbgrader_highlight_cls)) {
            cell.element.removeClass(nbgrader_highlight_cls);
        }
    });

    // update total points when a cell is deleted
    events.on("delete.Cell", function (evt, info) {
        update_total();
    });

    // validate cell ids on save
    events.on("before_save.Notebook", function (evt) {
        validate_ids();
    });

    var to_float = function(val) {
        if (val === undefined || val === "") {
            return 0;
        }
        return parseFloat(val);
    };

    var update_total = function() {
        var total_points = 0;
        var cells = Jupyter.notebook.get_cells();
        for (let cell of cells) {
            if (model.is_graded(cell)) {
                total_points += to_float(cell.metadata.nbgrader.points);
            }
        }
        $("#nbgrader-total-points").attr("value", total_points);
    };

    var validate_ids = function() {
        var elems, set, i, label;

        if (warning !== undefined) {
            return;
        }

        var valid = /^[a-zA-Z0-9_\-]+$/;
        var modal_opts = {
            notebook: Jupyter.notebook,
            keyboard_manager: Jupyter.keyboard_manager,
            buttons: {
                OK: {
                    class: "btn-primary",
                    click: function () {
                        warning = undefined;
                    }
                }
            }
        };

        elems = $(".nbgrader-id-input");
        set = new Object();
        for (i = 0; i < elems.length; i++) {
            label = $(elems[i]).val();
            if (!valid.test(label)) {
                modal_opts.title = "Invalid nbgrader cell ID";
                modal_opts.body = "At least one cell has an invalid nbgrader ID. Cell IDs must contain at least one character, and may only contain letters, numbers, hyphens, and/or underscores.";
                warning = dialog.modal(modal_opts);
                break;
            } else if (label in set) {
                modal_opts.title = "Duplicate nbgrader cell ID";
                modal_opts.body = "The nbgrader ID \"" + label + "\" has been used for more than one cell. Please make sure all grade cells have unique ids.";
                warning = dialog.modal(modal_opts);
                break;
            } else {
                set[label] = true;
            }
        }
    };

    var validate_schema_version = function() {
        var i, cells, schema;

        if (warning !== undefined) {
            return;
        }

        var modal_opts = {
            notebook: Jupyter.notebook,
            keyboard_manager: Jupyter.keyboard_manager,
            buttons: {
                OK: {
                    class: "btn-primary",
                    click: function () {
                        warning = undefined;
                    }
                }
            }
        };

        cells = Jupyter.notebook.get_cells();
        for (i = 0; i < cells.length; i++) {
            schema = model.get_schema_version(cells[i]);
            if (schema !== undefined && schema < nbgrader_schema_version) {
                modal_opts.title = "Outdated schema version";
                modal_opts.body = $("<p/>").html(
                    "At least one cell has an old version (" + schema + ") of the " +
                    "nbgrader metadata. Please back up this notebook and then " +
                    "update the metadata on the command " +
                    "line using the following command: <code>nbgrader update " +
                    Jupyter.notebook.notebook_path + "</code>");
                warning = dialog.modal(modal_opts);
                break;
            }
        }
    };

    var clear_cell_types = function() {
        var cells = Jupyter.notebook.get_cells();
        var i;
        for (i = 0; i < cells.length; i++) {
            if (cells[i].metadata.nbgrader !== undefined && cells[i].metadata.nbgrader.hasOwnProperty("cell_type")) {
                delete cells[i].metadata.nbgrader.cell_type;
            }
        }
    };

    

    /**
     * Add a display class to the cell element, depending on the
     * nbgrader cell type.
     */
    var display_cell = function (cell) {
        if (model.is_graded(cell) || model.is_solution(cell)) {
            if (cell.element && !cell.element.hasClass(nbgrader_highlight_cls)) {
                cell.element.addClass(nbgrader_highlight_cls);
            }
        }
        if (model.is_graded(cell) || model.is_solution(cell) || model.is_locked(cell)) {
            if (cell.element && !cell.element.hasClass(nbgrader_cls)) {
                cell.element.addClass(nbgrader_cls);
            }
        }

        if (model.is_task(cell) ){
          if (cell.element && !cell.element.hasClass("nbgrader_task")) {
                cell.element.addClass("nbgrader_task");
          }
        } else {
          if (cell.element && cell.element.hasClass("nbgrader_task")) {
                cell.element.removeClass("nbgrader_task");
          }
        }
    };

    var create_celltype_select = function (div, cell, celltoolbar) {
        // hack -- the DOM element for the celltoolbar is created before the
        // cell type is actually set, so we need to wait until the cell type
        // has been set before we can actually create the select menu
        if (cell.cell_type === null) {
            setTimeout(function () {
                create_celltype_select(div, cell, celltoolbar);
            }, 100);

        } else {

            if (model.is_invalid(cell)) {
                model.set_schema_version(cell);
                model.set_solution(cell, false);
                model.set_grade(cell, false);
                model.set_locked(cell, false);
                model.set_task(cell, false);
                celltoolbar.rebuild();
                return;
            }

            var options_list = [];
            options_list.push(["-", ""]);
            options_list.push(["Manually graded answer", "manual"]);
            options_list.push(["Manually graded task", "task"]);
            if (cell.cell_type == "markdown") {
                options_list.push(["Multiple Choice", "multiplechoice"]);
                options_list.push(["Single Choice", "singlechoice"]);
                options_list.push(["Diagram Cell", "diagram"]);
                options_list.push(["Upload answer", "attachments"]);
                options_list.push(["Read-only HTML", "pdf"]);
            }
            if (cell.cell_type == "code") {
                options_list.push(["Autograded answer", "solution"]);
                options_list.push(["Autograder tests", "tests"]);
            }
            options_list.push(["Read-only", "readonly"]);
            var setter = function (cell, val) {
                if (val === "") {
                    model.remove_metadata(cell);
                    extramodel.remove_metadata(cell);
                } else if (val === 'multiplechoice') {
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, true);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                    extramodel.to_multiplechoice(cell);
                    if (cell.rendered) {
                        cell.unrender_force();
                        cell.render();
                    }
                } else if (val === 'singlechoice') {
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, true);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                    extramodel.to_singlechoice(cell);
                    if (cell.rendered) {
                        cell.unrender_force();
                        cell.render();
                    }
                } else if (val === 'diagram') {
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, true);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                    extramodel.to_diagram(cell);
                    if (cell.rendered) {
                        cell.unrender_force();
                        cell.render();
                    }
                } else if (val === "attachments") {
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, true);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                    extramodel.to_attachment(cell);
                    if (cell.rendered) {
                        cell.unrender_force();
                        cell.render();
                    }
                } else if (val === "pdf") {
                    model.set_schema_version(cell);
                    model.set_solution(cell, false);
                    model.set_grade(cell, false);
                    model.set_locked(cell, true);
                    model.set_task(cell, false);
                    extramodel.to_pdf(cell);
                } else if (val === "manual") {
                    extramodel.remove_metadata(cell);
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, true);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                } else if (val === "task") {
                    extramodel.remove_metadata(cell);
                    model.set_schema_version(cell);
                    model.set_solution(cell, false);
                    model.set_grade(cell, false);
                    model.set_locked(cell, true);
                    model.set_task(cell, true);
                    if (cell.get_text() === ''){
                      cell.set_text('Describe the task here!')
                    }
                } else if (val === "solution") {
                    extramodel.remove_metadata(cell);
                    model.set_schema_version(cell);
                    model.set_solution(cell, true);
                    model.set_grade(cell, false);
                    model.set_locked(cell, false);
                    model.set_task(cell, false);
                } else if (val === "tests") {
                    extramodel.remove_metadata(cell);
                    model.set_schema_version(cell);
                    model.set_solution(cell, false);
                    model.set_grade(cell, true);
                    model.set_locked(cell, true);
                    model.set_task(cell, false);
                } else if (val === "readonly") {
                    extramodel.remove_metadata(cell);
                    model.set_schema_version(cell);
                    model.set_solution(cell, false);
                    model.set_grade(cell, false);
                    model.set_locked(cell, true);
                    model.set_task(cell, false);
                } else {
                    throw new Error("invalid nbgrader cell type: " + val);
                }
            };

            var getter = function (cell) {
                if (model.is_task(cell)) {
                    return "task";
                } else if (extramodel.is_multiplechoice(cell)) {
                    return "multiplechoice";
                } else if (extramodel.is_singlechoice(cell)) {
                    return "singlechoice";
                } else if (extramodel.is_attachment(cell)) {
                    return "attachments";
                } else if (extramodel.is_diagram(cell)) {
                    return "diagram";
                } else if (extramodel.is_pdf(cell)) {
                    return "pdf";
                } else if (model.is_solution(cell) && model.is_grade(cell)) {
                    return "manual";
                } else if (model.is_solution(cell) && cell.cell_type === "code") {
                    return "solution";
                } else if (model.is_grade(cell) && cell.cell_type === "code") {
                    return "tests";
                } else if (model.is_locked(cell)) {
                    return "readonly";
                } else {
                    return "";
                }
            };

            var select = $('<select/>');
            for (let option of options_list) {
                let opt = $('<option/>')
                    .attr('value', option[1])
                    .text(option[0]);
                select.append(opt);
            }
            select.val(getter(cell));
            select.change(function () {
                setter(cell, select.val());
                celltoolbar.rebuild();
                update_total();
                display_cell(cell);
            });
            display_cell(cell);
            $(div).append($('<span/>').append(select));
        }
    };

    /**
     * Create the input text box for the problem or test id.
     */
    var create_id_input = function (div, cell, celltoolbar) {
        if (!model.is_grade(cell) && !model.is_solution(cell) && !model.is_locked(cell)) {
            return;
        }
        if (model.is_invalid(cell)) {
            return;
        }

        var local_div = $('<div/>');
        var text = $('<input/>').attr('type', 'text');
        var lbl = $('<label/>').append($('<span/>').text('ID: '));
        lbl.append(text);

        model.set_grade_id(cell, model.get_grade_id(cell));
        text.addClass('nbgrader-id-input');
        text.attr("value", model.get_grade_id(cell));
        text.change(function () {
            model.set_grade_id(cell, text.val());
        });

        local_div.addClass('nbgrader-id');
        $(div).append(local_div.append($('<span/>').append(lbl)));

        Jupyter.keyboard_manager.register_events(text);
    };

    /**
     * Create the input text box for the number of points the problem
     * is worth.
     */
    var create_points_input = function (div, cell, celltoolbar) {
        if (!model.is_graded(cell) || model.is_invalid(cell)) {
            return;
        }

        var local_div = $('<div/>');
        var text = $('<input/>').attr('type', 'number');
        var lbl = $('<label/>').append($('<span/>').text('Points: '));
        lbl.append(text);

        text.addClass('nbgrader-points-input');
        text.attr("value", model.get_points(cell));
        model.set_points(cell, model.get_points(cell));
        update_total();

        text.change(function () {
            model.set_points(cell, text.val());
            text.val(model.get_points(cell));
            update_total();
        });

        local_div.addClass('nbgrader-points');
        $(div).append(local_div.append($('<span/>').append(lbl)));

        Jupyter.keyboard_manager.register_events(text);
    };

    var create_lock_cell_button = function (div, cell, celltoolbar) {
        var lock = $("<a />").addClass("lock-button");
        if (model.is_locked(cell)) {
            lock.append($("<li />").addClass("fa fa-lock"));
            lock.tooltip({
                placement: "right",
                title: "Student changes will be overwritten"
            });
        }

        $(div).addClass("lock-cell-container").append(lock);
    };

    /**
     * Load custom css for the nbgrader toolbar.
     */
    var load_css = function () {
        var link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./create_assignment.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    };

    /**
     * Load the nbgrader toolbar extension.
     */
    var load_extension = function () {
        load_css();
        let static_path = Jupyter.notebook.base_url + 'e2xbase/static/js/models/';
        require([static_path + 'extracell.js', static_path + 'nbgrader.js'], function(extracell, nbgrader) {
            extramodel = extracell;
            model = nbgrader;
            
            CellToolbar.register_callback('create_assignment.grading_options', create_celltype_select);
            CellToolbar.register_callback('create_assignment.id_input', create_id_input);
            CellToolbar.register_callback('create_assignment.points_input', create_points_input);
            CellToolbar.register_callback('create_assignment.lock_cell', create_lock_cell_button);

            var preset = [
                'create_assignment.lock_cell',
                'create_assignment.points_input',
                'create_assignment.id_input',
                'create_assignment.grading_options',
            ];
            CellToolbar.register_preset(nbgrader_preset_name, preset, Jupyter.notebook);
            console.log('nbgrader extension for metadata editing loaded.');
        });
        
    };

    return {
        'load_ipython_extension': load_extension
    };
});
