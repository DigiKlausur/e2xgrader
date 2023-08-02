import $ from "jquery";
import Jupyter from "base/js/namespace";
import { Menubar } from "@e2xgrader/menubar";
import { urlJoin, requests } from "@e2xgrader/api";
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

  add_help() {
    let that = this;
    let dropwdown_content = [];
    requests
      .get(urlJoin(Jupyter.notebook.base_url, "e2x/help/api/files"))
      .then((data) => {
        data.forEach(function (entry) {
          dropwdown_content.push({
            label: entry[0],
            callback: function () {
              window.open(
                urlJoin(
                  Jupyter.notebook.base_url,
                  "e2x/help/static/",
                  entry[1]
                ),
                "_blank"
              );
            },
          });
        });
      })
      .finally(() => {
        if (dropwdown_content.length > 0) {
          that.add_dropdown("help", "Additional Resources", dropwdown_content);
        }
        that.element.append(
          $("<div/>")
            .addClass("e2x-button e2x-submit")
            .on("click", function () {
              that.submit.prepare_submit();
            })
            .append("Submit")
            .append($("<i/>").addClass("fa fa-paper-plane"))
        );
      });
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
    this.add_help();
    this.add_divider();

    super.activate();
  }
}
