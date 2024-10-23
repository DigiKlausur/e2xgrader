import { Menubar } from "@e2xgrader/menubar";
import { insert_cells, get_file_options, set_template_ids } from "./utils";
import { manage_tags } from "./dialogs";
import { utils } from "@e2xgrader/utils";
import API from "./api";

export class TemplateMenubar extends Menubar {
  constructor() {
    super();
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
    API.get_template_preset(name).then((res) => {
      const cells = res.data;
      set_template_ids(cells, utils.randomString(8));
      insert_cells(cells);
    });
  }

  activate() {
    API.list_template_presets().then((presets) => {
      this.presets = presets.data;
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
