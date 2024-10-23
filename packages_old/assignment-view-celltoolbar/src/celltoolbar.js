import _ from "underscore";
import $ from "jquery";
import Jupyter from "base/js/namespace";
import events from "base/js/events";
import { CellToolbar } from "notebook/js/celltoolbar";
import { utils as nbgrader_utils } from "@e2xgrader/utils";
import { utils as e2xutils } from "@e2xgrader/cells";

import "./assignment-view.css";

export class AssignmentViewToolbar {
  /**
   * Create and register the AssignmentViewToolbar
   * This adds highlights to solution and description cells
   */
  constructor() {
    this.highlight = "highlight";
    this.minimized = "minimized";
    this.preset_name = "Assignment View";
    this.initialize_events();

    // Register callbacks
    this.register();
  }

  /**
   * Register the AssignmentViewToolbar preset
   */
  register() {
    if (CellToolbar._presets.hasOwnProperty(this.preset_name)) {
      return;
    }
    CellToolbar.register_callback(
      "assignment_view.create_header",
      _.bind(this.create_header, this),
    );
    let preset = ["assignment_view.create_header"];
    CellToolbar.register_preset(this.preset_name, preset, Jupyter.notebook);
  }

  /**
   * Activate the AssignmentViewToolbar
   */
  activate() {
    // Activate the toolbar
    CellToolbar.activate_preset(this.preset_name);
    Jupyter.CellToolbar.global_show();
  }

  /**
   * Initialize the events associated with this toolbar
   */
  initialize_events() {
    let that = this;
    events.on("preset_activated.CellToolbar", function (evt, preset) {
      if (preset.name != that.preset_name) {
        for (const cell of Jupyter.notebook.get_cells()) {
          that.remove_classes(cell);
        }
      }
    });
  }

  /**
   * Add the highlight CSS class to the celltoolbar
   *
   * @param  {Cell}
   */
  add_highlight(cell) {
    if (cell.celltoolbar !== undefined) {
      if (!cell.celltoolbar.inner_element.hasClass(this.highlight)) {
        cell.celltoolbar.inner_element.addClass(this.highlight);
      }
    }
  }

  /**
   * Add the hidden CSS class to the celltoolbar
   *
   * @param  {Cell}
   */
  add_hidden(cell) {
    if (cell.celltoolbar !== undefined) {
      if (!cell.celltoolbar.inner_element.hasClass(this.minimized)) {
        cell.celltoolbar.inner_element.addClass(this.minimized);
      }
    }
  }

  /**
   * Remove the celltoolbar CSS classes
   *
   * @param  {Cell}
   */
  remove_classes(cell) {
    if (cell.celltoolbar !== null && cell.celltoolbar !== undefined) {
      if (cell.celltoolbar.inner_element.hasClass(this.highlight)) {
        cell.celltoolbar.inner_element.removeClass(this.highlight);
      } else if (cell.celltoolbar.inner_element.hasClass(this.minimized)) {
        cell.celltoolbar.inner_element.removeClass(this.minimized);
      }
    }
  }

  /**
   * Create a button
   *
   * @param  {string} btn_text   - text for the button
   * @param  {string} btn_id     - id for the button
   * @param  {function} callback - callback when button is clicked
   * @return {HTMLElement} button
   */
  create_button(btn_text, btn_id, callback) {
    let btn = $("<button/>")
      .attr("type", "button")
      .attr("id", btn_id)
      .addClass("exam_btn")
      .text(btn_text);
    btn.on("click", callback);
    return btn;
  }

  /**
   * Create a header for the cell
   *
   * @param  {HTMLElement} div - the cell div
   * @param  {Cell}
   * @param  {CellToolbar} celltoolbar
   */
  create_header(div, cell, celltoolbar) {
    if (cell.cell_type === null) {
      let that = this;
      setTimeout(function () {
        that.create_header(div, cell, celltoolbar);
      }, 100);
    } else {
      if (!nbgrader_utils.is_solution(cell)) {
        this.remove_classes(cell);
        this.add_hidden(cell);
        return;
      }
      this.add_highlight(cell);
      if (e2xutils.is_e2x(cell)) {
        return;
      }
      if (cell.cell_type === "code") {
        let btn = this.create_button("Run", "run", function () {
          cell.execute();
        });
        $(div).append($("<span/>").append(btn).addClass("cell_control"));
      } else if (cell.cell_type === "markdown") {
        let edit_btn = this.create_button("Edit", "edit", function () {
          cell.events.trigger("select.Cell", { cell: cell });
          Jupyter.notebook.edit_mode();
          celltoolbar.rebuild();
        });
        let btn = this.create_button("Preview", "preview", function () {
          cell.execute();
          celltoolbar.rebuild();
        });
        $(div).append(
          $("<span/>").append(edit_btn).append(btn).addClass("cell_control"),
        );
      }
    }
  }
}
