import $ from "jquery";
import Jupyter from "base/js/namespace";
import utils from "base/js/utils";

/**
 * Append a link to the tree view's tab bar that opens in a new browser tab.
 *
 * @param {string} text - Label shown on the tab.
 * @param {...string} path_parts - URL path segments, joined onto the base URL.
 */
export function add_tab_link(text, ...path_parts) {
  if (!Jupyter.notebook_list) {
    return;
  }
  const href = utils.url_path_join(
    Jupyter.notebook_list.base_url,
    ...path_parts
  );
  $("#tabs").append(
    $("<li/>").append(
      $("<a/>").attr("href", href).attr("target", "_blank").text(text)
    )
  );
}
