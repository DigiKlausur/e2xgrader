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
    Object.keys(this.options).forEach((key) => {
      if (!current_options.hasOwnProperty(key)) {
        current_options[key] = this.options[key];
      }
    });
    set_e2x_field(this.cell, "options", current_options);
  }

  get_option(key) {
    let options = get_e2x_field(this.cell, "options");
    if (options.hasOwnProperty(key)) {
      return options[key];
    }
    return this.options[key]["value"];
  }

  set_option(key, value) {
    console.log("Setting options", key, value);
    let options = get_e2x_field(this.cell, "options");
    options[key]["value"] = value;
    set_e2x_field(this.cell, "options", options);
  }

  render() {
    let that = this;
    let container = $("<div/>").addClass("e2x_options");

    for (const [key, value] of Object.entries(
      get_e2x_field(this.cell, "options"),
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
