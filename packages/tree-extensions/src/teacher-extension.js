import $ from "jquery";
import Jupyter from "base/js/namespace";

export function load_ipython_extension() {
  if (!Jupyter.notebook_list) {
    return;
  }
  $("#tabs").append(
    $("<li/>").append(
      $("<a/>")
        .attr("href", Jupyter.notebook_list.base_url + "taskcreator")
        .attr("target", "_blank")
        .text("Authoring")
    )
  );
}
