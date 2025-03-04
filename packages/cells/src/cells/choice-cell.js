import Jupyter from "base/js/namespace";
import { E2xCell } from "./base";
import { get_e2x_field, set_e2x_field } from "../utils/e2x-utils";

class ChoiceCell extends E2xCell {
  constructor(cell, type) {
    super(cell, type);
    this.choice_field = "choice";
  }

  set_choice(value) {
    set_e2x_field(this.cell, this.choice_field, value);
  }

  get_choices() {
    return get_e2x_field(this.cell, this.choice_field, []);
  }
}

export class SinglechoiceCell extends ChoiceCell {
  constructor(cell) {
    super(cell, "singlechoice");
  }

  create_radio_button(name, value, selected, onChange) {
    let input = $("<input>")
      .attr("type", "radio")
      .attr("name", name)
      .attr("value", value)
      .on("change", onChange);
    if (selected) {
      input.attr("checked", "checked");
    }
    return input;
  }

  render() {
    this.cell.render_force();
    let html = $(this.cell.element).find(".rendered_html");
    let lists = html.find("ul");
    let choices = this.get_choices();
    let that = this;
    if (lists.length > 0) {
      let list = lists[0];
      let form = $("<form>").addClass("hbrs_radio");
      let items = $(list).find("li");
      if (choices.length > 0 && choices[0] >= items.length) {
        let metadata = this.get_metadata();
        metadata[this.choice_field] = [];
        choices = this.get_choices();
      }
      for (let i = 0; i < items.length; i++) {
        let input = this.create_radio_button(
          "my_radio",
          i,
          choices.indexOf(i.toString()) >= 0,
          function () {
            that.set_choice(this.value);
            Jupyter.notebook.set_dirty(true);
          }
        );
        Jupyter.keyboard_manager.register_events(input);
        form.append(
          $("<div>")
            .append(input)
            .append("&nbsp;&nbsp;")
            .append(items[i].childNodes)
        );
      }
      $(list).replaceWith(form);
    }
    this.render_grader_settings();
  }
}

export class MultiplechoiceCell extends ChoiceCell {
  constructor(cell) {
    super(cell, "multiplechoice");
    this.choice_count_field = "num_of_choices";
  }

  get_number_of_choices() {
    return get_e2x_field(this.cell, this.choice_count_field, []);
  }

  set_number_of_choices(value) {
    set_e2x_field(this.cell, this.choice_count_field, value);
  }

  add_choice(value) {
    let choices = this.get_choices();
    let idx = choices.indexOf(value);
    if (idx > -1) {
      return;
    }
    choices.push(value);
    this.set_choice(choices);
  }

  remove_choice(value) {
    let choices = this.get_choices();
    let idx = choices.indexOf(value);
    if (idx > -1) {
      choices.splice(idx, 1);
    }
    this.set_choice(choices);
  }

  create_checkbox(name, value, selected) {
    let that = this;
    let input = $("<input>")
      .attr("type", "checkbox")
      .attr("name", name)
      .attr("value", value)
      .on("change", function () {
        if (this.checked) {
          that.add_choice(this.value);
        } else {
          that.remove_choice(this.value);
        }
        Jupyter.notebook.set_dirty(true);
      });
    if (selected) {
      input.attr("checked", "checked");
    }
    return input;
  }

  render() {
    this.cell.render_force();
    let html = $(this.cell.element).find(".rendered_html");
    let lists = html.find("ul");

    if (lists.length > 0) {
      let list = lists[0];
      let form = $("<form>").addClass("hbrs_checkbox");
      let items = $(list).find("li");
      let num_of_choices = this.get_number_of_choices();
      if (num_of_choices != items.length) {
        this.set_number_of_choices(items.length);
        let metadata = this.get_metadata();
        metadata[this.choice_field] = [];
      }
      let choices = this.get_choices();
      for (let i = 0; i < items.length; i++) {
        let input = this.create_checkbox(
          "my_checkbox",
          i,
          choices.indexOf(i.toString()) >= 0
        );
        Jupyter.keyboard_manager.register_events(input);

        let input_div = $("<div>")
          .append(input)
          .append("&nbsp;&nbsp;")
          .append(items[i].childNodes);

        form.append(input_div);
      }
      $(list).replaceWith(form);
    }
    this.render_grader_settings();
  }
}
