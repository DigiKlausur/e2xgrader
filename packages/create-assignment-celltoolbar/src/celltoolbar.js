import _ from "underscore";
import $ from "jquery";
import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { CellToolbar } from "notebook/js/celltoolbar";
import { NbgraderValidator } from "./validator";
import { CellFactory } from "./cellfactory";
import "./create-assignment.css";
import { utils } from "@e2xgrader/utils";

console.log(utils);
const old_global_hide = CellToolbar.global_hide;
const old_rebuild = CellToolbar.prototype.rebuild;

export class CreateAssignmentToolbar {
  /**
   * Create and register the CreateAssignmentToolbar
   * This adds functioniality for creating assignments
   */
  constructor() {
    this.highlight = "nbgrader-highlight";
    this.cell_cls = "nbgrader-cell";
    this.task_cls = "nbgrader_task";
    this.preset_name = "Create Assignment";
    this.validator = new NbgraderValidator();
    this.cellfactory = new CellFactory();

    this.patch_celltoolbar();
    this.initialize_events();
  }

  patch_celltoolbar() {
    // trigger an event when the toolbar is being rebuilt
    CellToolbar.prototype._rebuild = old_rebuild;
    CellToolbar.prototype.rebuild = function () {
      events.trigger("toolbar_rebuild.CellToolbar", this.cell);
      this._rebuild();
    };

    // trigger an event when the toolbar is being (globally) hidden
    //CellToolbar._global_hide = CellToolbar.global_hide;
    CellToolbar.global_hide = function () {
      $("#nbgrader-total-points-group").hide();

      old_global_hide();
      for (let instance of CellToolbar._instances) {
        events.trigger("global_hide.CellToolbar", instance.cell);
      }
    };
  }

  clear_cell_types() {
    for (let cell of Jupyter.notebook.get_cells()) {
      utils.remove_nbgrader_field(cell, "cell_type");
    }
  }

  initialize_events() {
    let that = this;
    // show the total points when the preset is activated
    events.on("preset_activated.CellToolbar", function (evt, preset) {
      that.validator.validate_schema_version();
      that.clear_cell_types();

      let elem = $("#nbgrader-total-points-group");
      if (preset.name === that.preset_name) {
        if (elem.length == 0) {
          elem = $("<div />").attr("id", "nbgrader-total-points-group");
          elem.addClass("btn-group");
          elem.append($("<span />").text("Total points:"));
          elem.append(
            $("<input />")
              .attr("disabled", "disabled")
              .attr("type", "number")
              .attr("id", "nbgrader-total-points")
          );
          $("#maintoolbar-container").append(elem);
        }
        elem.show();
        that.update_total_points();
      } else {
        elem.hide();
      }
    });

    // remove nbgrader class when the cell is either hidden or rebuilt
    events.on(
      "global_hide.CellToolbar toolbar_rebuild.CellToolbar",
      function (evt, cell) {
        if (cell.element && cell.element.hasClass(that.cell_cls)) {
          cell.element.removeClass(that.cell_cls);
        }
        if (cell.element && cell.element.hasClass(that.highlight)) {
          cell.element.removeClass(that.highlight);
        }
      }
    );

    // update total points when a cell is deleted
    events.on("delete.Cell", function (evt, info) {
      that.update_total_points();
    });

    // validate cell ids on save
    events.on("before_save.Notebook", function (evt) {
      that.validator.validate_ids();
    });
  }

  register() {
    if (CellToolbar._presets.hasOwnProperty(this.preset_name)) {
      return;
    }
    CellToolbar.register_callback(
      "create_assignment.grading_options",
      _.bind(this.create_celltype_select, this)
    );
    CellToolbar.register_callback(
      "create_assignment.id_input",
      _.bind(this.create_id_input, this)
    );
    CellToolbar.register_callback(
      "create_assignment.points_input",
      _.bind(this.create_points_input, this)
    );
    CellToolbar.register_callback(
      "create_assignment.lock_cell",
      _.bind(this.create_lock_cell_button, this)
    );

    let preset = [
      "create_assignment.lock_cell",
      "create_assignment.points_input",
      "create_assignment.id_input",
      "create_assignment.grading_options",
    ];
    CellToolbar.register_preset(this.preset_name, preset, Jupyter.notebook);
  }

  /**
   * Activate the toolbar
   */
  activate() {
    this.register();
    CellToolbar.activate_preset(this.preset_name);
    Jupyter.CellToolbar.global_show();
  }

  update_total_points() {
    let total_points = 0;
    let cells = Jupyter.notebook.get_cells();
    for (let cell of cells) {
      if (utils.is_grade(cell) || utils.is_task(cell)) {
        total_points += utils.get_points(cell);
      }
    }
    $("#nbgrader-total-points").attr("value", total_points);
  }

  /**
   * Add a display class to the cell element, depending on the
   * nbgrader cell type.
   */
  display_cell(cell) {
    if (
      utils.is_grade(cell) ||
      utils.is_task(cell) ||
      utils.is_solution(cell)
    ) {
      if (cell.element && !cell.element.hasClass(this.highlight)) {
        cell.element.addClass(this.highlight);
      }
    }
    if (
      utils.is_grade(cell) ||
      utils.is_task(cell) ||
      utils.is_solution(cell) ||
      utils.is_locked(cell)
    ) {
      if (cell.element && !cell.element.hasClass(this.cell_cls)) {
        cell.element.addClass(this.cell_cls);
      }
    }

    if (utils.is_task(cell)) {
      if (cell.element && !cell.element.hasClass(this.task_cls)) {
        cell.element.addClass(this.task_cls);
      }
    } else {
      if (cell.element && cell.element.hasClass(this.task_cls)) {
        cell.element.removeClass(this.task_cls);
      }
    }
  }

  /**
   * Create the input text box for the problem or test id.
   */
  create_id_input(div, cell, celltoolbar) {
    if (
      !utils.is_grade(cell) &&
      !utils.is_solution(cell) &&
      !utils.is_locked(cell)
    ) {
      return;
    }
    if (utils.is_invalid(cell)) {
      return;
    }

    let local_div = $("<div/>");
    let text = $("<input/>").attr("type", "text");
    let lbl = $("<label/>").append($("<span/>").text("ID: "));
    lbl.append(text);

    utils.set_grade_id(cell, utils.get_grade_id(cell));
    text.addClass("nbgrader-id-input");
    text.attr("value", utils.get_grade_id(cell));
    text.on("change", function () {
      utils.set_grade_id(cell, text.val());
    });

    local_div.addClass("nbgrader-id");
    $(div).append(local_div.append($("<span/>").append(lbl)));

    Jupyter.keyboard_manager.register_events(text);
  }

  /**
   * Create the input text box for the number of points the problem
   * is worth.
   */
  create_points_input(div, cell, celltoolbar) {
    if (
      !(utils.is_grade(cell) || utils.is_task(cell)) ||
      utils.is_invalid(cell)
    ) {
      return;
    }

    let that = this;

    let local_div = $("<div/>");
    let text = $("<input/>").attr("type", "number");
    let lbl = $("<label/>").append($("<span/>").text("Points: "));
    lbl.append(text);

    text.addClass("nbgrader-points-input");
    text.attr("value", utils.get_points(cell));
    utils.set_points(cell, utils.get_points(cell));
    this.update_total_points();

    text.on("change", function () {
      utils.set_points(cell, text.val());
      text.val(utils.get_points(cell));
      that.update_total_points();
    });

    local_div.addClass("nbgrader-points");
    $(div).append(local_div.append($("<span/>").append(lbl)));

    Jupyter.keyboard_manager.register_events(text);
  }

  create_lock_cell_button(div, cell, celltoolbar) {
    let lock = $("<a />").addClass("lock-button");
    if (utils.is_locked(cell)) {
      lock.append($("<li />").addClass("fa fa-lock"));
      lock.tooltip({
        placement: "right",
        title: "Student changes will be overwritten",
      });
    }

    $(div).addClass("lock-cell-container").append(lock);
  }

  create_celltype_select(div, cell, celltoolbar) {
    let that = this;
    if (cell.cell_type === null) {
      setTimeout(function () {
        that.create_celltype_select(div, cell, celltoolbar);
      }, 100);
    } else {
      if (utils.is_invalid(cell)) {
        utils.set_schema_version(cell);
        utils.set_solution(cell, false);
        utils.set_grade(cell, false);
        utils.set_locked(cell, false);
        utils.set_task(cell, false);
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
        options_list.push(["Upload answer", "attachments"]);
        options_list.push(["Diagram answer", "diagram"]);
        options_list.push(["Read-only HTML", "pdf"]);
      }
      if (cell.cell_type == "code") {
        options_list.push(["Autograded answer", "solution"]);
        options_list.push(["Autograder tests", "tests"]);
      }
      options_list.push(["Read-only", "readonly"]);
      var setter = function (cell, val) {
        that.cellfactory.to_cell(cell, val);
      };

      var getter = function (cell) {
        return that.cellfactory.get_type(cell);
      };

      var select = $("<select/>");
      for (let option of options_list) {
        let opt = $("<option/>").attr("value", option[1]).text(option[0]);
        select.append(opt);
      }
      select.val(getter(cell));
      select.on("change", function () {
        setter(cell, select.val());
        celltoolbar.rebuild();
        that.update_total_points();
        that.display_cell(cell);
      });
      that.display_cell(cell);
      $(div).append($("<span/>").append(select));
    }
  }
}
