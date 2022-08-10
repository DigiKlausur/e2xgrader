import $ from "jquery";
import Jupyter from "base/js/namespace";
import { Menubar } from "@e2xgrader/menubar";
import { Submit } from "./submit";
import "./exam-menubar.css";

export class ExamMenubar extends Menubar {
  constructor() {
    super();
    this.submit = new Submit();
  }

  add_kernel_indiciator() {
    this.element.append(
      $("<span/>")
        .css("padding", "0 1em 0 1em")
        .append($(".kernel_indicator_name").css("padding-left", ".5em"))
        .append($("#kernel_indicator_icon").css("padding-left", ".5em"))
    );
  }

  activate() {
    this.add_save_button();
    this.add_divider();
    this.add_run_controls();
    this.add_divider();
    this.add_kernel_indiciator();
    this.add_divider();
    this.add_spacer();
    this.add_divider();
    this.add_dropdown("advanced-options", "Advanced", [
      {
        label: "Clear All Outputs",
        callback: function () {
          Jupyter.notebook.clear_all_output();
        },
      },
    ]);
    this.add_divider();
    let that = this;
    this.element.append(
      $("<div/>")
        .addClass("e2x-button e2x-submit")
        .on("click", function () {
          that.submit.prepare_submit();
        })
        .append("Submit")
        .append($("<i/>").addClass("fa fa-paper-plane"))
    );
    super.activate();
  }
}
