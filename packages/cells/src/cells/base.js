import $ from "jquery";
import { create_e2x_metadata, get_e2x_metadata } from "../utils/e2x-utils";
import { OptionDict } from "../utils/option-dict";

export class E2xCell {
  /**
   * Creates an instance of E2xCell.
   * @param {Object} cell - The cell object to be modified.
   * @param {string} type - The type of cell.
   * @param {Object} [options={}] - The options for the cell.
   */
  constructor(cell, type, options = {}) {
    this.type = type;
    this.cell = cell;
    create_e2x_metadata(this.cell, this.type);
    this.option_dict = new OptionDict(this.cell, options);
  }

  /**
   * Returns the e2x metadata for the cell.
   * @returns {Object} The e2x metadata for the cell.
   */
  get_metadata() {
    return get_e2x_metadata(this.cell);
  }

  /**
   * Renders the cell.
   */
  render() {
    this.cell.render();
  }

  /**
   * Renders the grader settings for the cell if in edit mode.
   */
  render_grader_settings() {
    if (!this.edit_mode) {
      return;
    }
    let that = this;
    let html = $(this.cell.element).find(".rendered_html");
    // Remove old div
    html.find(".e2x_grader_options").remove();
    let container = $("<div/>").addClass("e2x_grader_options");

    container.append($("<hr/>"));

    container.append(this.option_dict.render());
    container.append(
      $("<button/>")
        .attr("type", "button")
        .addClass("e2x_unrender")
        .addClass("btn-e2x")
        .on("click", function () {
          that.cell.unrender_force();
          that.cell.keyboard_manager.enable();
        })
        .append("Edit cell")
    );
    html.append(container);
  }
}
