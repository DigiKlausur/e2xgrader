import $ from "jquery";
import Jupyter from "base/js/namespace";
import utils from "base/js/utils";
import { load_help_tab } from "@e2xgrader/help-tab";

export function load_ipython_extension() {
  load_help_tab();
  if (!Jupyter.notebook_list) {
    return;
  }
  $("#tabs").append(
    $("<li/>").append(
      $("<a/>")
        .attr(
          "href",
          utils.url_path_join(
            Jupyter.notebook_list.base_url,
            "e2x",
            "authoring",
            "app",
          ),
        )
        .attr("target", "_blank")
        .text("Authoring"),
    ),
  );
}
