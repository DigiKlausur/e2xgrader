import $ from "jquery";
import { get_e2x_field, set_e2x_field } from "./e2x-utils";

export class OptionDict {
  /**
   * Represents a dictionary of options for an E2xCell object.
   * @class
   * @param {E2xCell} cell - The E2xCell object.
   * @param {Object} options - The options for the cell.
   */
  constructor(cell, options) {
    this.cell = cell;
    this.options = options;
    this.initialize_options();
  }

  /**
   * Initializes options and makes sure they are in sync with cell metadata.
   */
  initialize_options() {
    let current_options = get_e2x_field(this.cell, "options");
    // Make sure the options of the cell are in sync
    let to_remove = [];
    Object.keys(current_options).forEach((key) => {
      if (!this.options.hasOwnProperty(key)) {
        to_remove.push(key);
      }
    });
    to_remove.forEach((key) => delete current_options[key]);
    Object.keys(this.options).forEach((key) => {
      if (!current_options.hasOwnProperty(key)) {
        current_options[key] = this.options[key];
      }
    });
    set_e2x_field(this.cell, "options", current_options);
  }

  /**
   * Gets the value of an option given its key.
   * @param {string} key - The key of the option.
   * @returns {any} - The value of the option.
   */
  get_option(key) {
    let options = get_e2x_field(this.cell, "options");
    if (options.hasOwnProperty(key)) {
      return options[key];
    }
    return this.options[key]["value"];
  }

  /**
   * Sets the value of an option given its key.
   * @param {string} key - The key of the option.
   * @param {any} value - The value to set for the option.
   */
  set_option(key, value) {
    console.log("Setting options", key, value);
    let options = get_e2x_field(this.cell, "options");
    options[key]["value"] = value;
    set_e2x_field(this.cell, "options", options);
  }

  /**
   * Renders the option dictionary as HTML.
   * @returns {JQuery<HTMLElement>} - The rendered HTML container element.
   */
  render() {
    let that = this;
    let container = $("<div/>").addClass("e2x_options");

    for (const [key, value] of Object.entries(
      get_e2x_field(this.cell, "options")
    )) {
      if (value["type"] == "checkbox") {
        let node = $("<div/>");
        let input = $("<input/>").attr("type", value["type"]);
        node.append(input);
        node.append($("<span/>").text(value["text"]));

        if (value["value"]) {
          input.attr("checked", "checked");
        }
        input.on("change", function () {
          that.set_option(key, !!this.checked);
        });
        container.append(node);
      }
    }
    return container;
  }
}
