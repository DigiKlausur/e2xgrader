define(["jquery", "./options"], function ($, option_dict) {
  "use strict";

  class ExtendedCell {
    constructor(cell, type, options = {}) {
      this.field = "extended_cell";
      this.type = type;
      this.cell = cell;

      if (!this.cell.metadata.hasOwnProperty(this.field)) {
        this.cell.metadata[this.field] = {};
      }
      this.cell.metadata[this.field]["type"] = type;
      this.option_dict = new option_dict.OptionDict(cell, options);
      this.edit_mode = false;
    }

    get_metadata() {
      if (this.cell.metadata.hasOwnProperty(this.field)) {
        return this.cell.metadata[this.field];
      }
      return {};
    }

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
          .click(function () {
            that.cell.unrender_force();
            that.cell.keyboard_manager.enable();
          })
          .append("Edit cell")
      );
      html.append(container);
    }

    render() {
      this.cell.render();
    }
  }

  return {
    ExtendedCell: ExtendedCell,
  };
});
