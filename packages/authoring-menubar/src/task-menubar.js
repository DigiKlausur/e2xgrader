import Jupyter from "base/js/namespace";
import { Menubar } from "@e2xgrader/menubar";
import { manage_tags, insert_question_preset_dialog } from "./dialogs";
import { AuthoringAPI } from "@e2xgrader/api";
import { get_file_options, insert_cells, set_task_ids } from "./utils";

export class TaskMenubar extends Menubar {
  constructor() {
    super();
    this.api = new AuthoringAPI(Jupyter.notebook.base_url);
    this.presets = [];
  }

  add_question_menu() {
    let menu_options = [];
    this.presets.forEach((name) => {
      menu_options.push({
        label: name,
        callback: () => this.insert_question_preset(name),
      });
    });
    this.add_dropdown("e2x-question-menu", "Add Question", menu_options);
  }

  insert_question_preset(name) {
    this.api.get_question_preset(name).then((res) => {
      const cells = res.data;
      insert_question_preset_dialog(name, (task_name, points) => {
        set_task_ids(cells, task_name, points);
        insert_cells(cells);
      });
    });
  }

  activate() {
    this.api.list_question_presets().then((presets) => {
      this.presets = presets.data;
      this.add_save_button();
      this.add_divider();
      this.add_question_menu();
      this.add_divider();
      this.add_dropdown("e2x-file-menu", "Add Files", get_file_options());
      this.add_divider();
      this.add_button("Manage Tags", manage_tags);
      this.add_divider();
      this.add_spacer();
      this.add_divider();
      this.add_run_controls();
      this.add_divider();
      this.element.append($("#move_up_down"));
      this.add_divider();
      let nbgrader_points = $("#nbgrader-total-points-group");
      nbgrader_points.css("padding", "0 1em 0 1em");
      this.element.append(nbgrader_points);
      super.activate();
      $("<div/>")
        .attr("id", "e2x-header")
        .append($("<span/>").text("Task"))
        .insertAfter($("#ipython_notebook"));
    });
  }
}
