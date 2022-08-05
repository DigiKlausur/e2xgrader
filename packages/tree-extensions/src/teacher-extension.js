import $ from "jquery";
import Jupyter from "base/js/namespace";
import utils from "base/js/utils";

export function load_ipython_extension() {
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
            "app"
          )
        )
        .attr("target", "_blank")
        .text("Authoring")
    )
  );
}
