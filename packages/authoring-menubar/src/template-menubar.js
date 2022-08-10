import Jupyter from "base/js/namespace";
import { Menubar } from "@e2xgrader/menubar";
import { AuthoringAPI } from "@e2xgrader/api";
import {
  insert_cells,
  get_file_options,
  set_template_ids,
  manage_tags,
} from "./utils";
import { utils } from "@e2xgrader/utils";

export class TemplateMenubar extends Menubar {
  constructor() {
    super();
    this.api = new AuthoringAPI(Jupyter.notebook.base_url);
    this.presets = [];
  }

  add_template_menu() {
    let menu_options = [];
    this.presets.forEach((name) => {
      menu_options.push({
        label: name,
        callback: () => this.insert_template_preset(name),
      });
    });
    this.add_dropdown("e2x-question-menu", "Add Cell", menu_options);
  }

  insert_template_preset(name) {
    this.api.get_template_preset(name).then((cells) => {
      set_template_ids(cells, utils.randomString(8));
      insert_cells(cells);
    });
  }

  activate() {
    this.api.list_template_presets().then((presets) => {
      this.presets = presets;
      this.add_save_button();
      this.add_divider();
      this.add_template_menu();
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
      super.activate();
      $("<div/>")
        .attr("id", "e2x-header")
        .append($("<span/>").text("Template"))
        .insertAfter($("#ipython_notebook"));
    });
  }
}
