import $ from "jquery";
import { get_e2x_field, set_e2x_field } from "./e2x-utils";

export class OptionDict {
  constructor(cell, options) {
    this.cell = cell;
    this.options = options;
    this.initialize_options();
  }

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
    set_e2x_field(this.cell, "options", current_options);
  }

  get_option(key) {
    let options = get_e2x_field(this.cell, "options");
    if (options.hasOwnProperty(key)) {
      return options[key];
    }
    return this.options[key]["value"];
  }

  render() {
    let that = this;
    let container = $("<div/>").addClass("e2x_options");

    for (const [key, value] of Object.entries(this.options)) {
      if (value["type"] == "checkbox") {
        let node = $("<div/>");
        let input = $("<input/>").attr("type", value["type"]);
        node.append(input);
        node.append($("<span/>").text(value["text"]));

        if (this.get_option(key)) {
          input.attr("checked", "checked");
        }
        input.on("change", () => that.set_option(key, !!this.checked));
        container.append(node);
      }
    }
    return container;
  }
}
