import $ from "jquery";
import { add_unsafe_renderer } from "./renderers";
import {
  patch_TextCell_toJSON,
  patch_Notebook_to_markdown,
  patch_MarkdownCell_render,
  patch_MarkdownCell_unrender,
  render_e2x_cells,
} from "./utils";
import "./extra_cells.css";

export function initialize_cell_extension() {
  $.event.special.destroyed = {
    remove: function (o) {
      if (o.handler) {
        o.handler();
      }
    },
  };
  add_unsafe_renderer();
  patch_TextCell_toJSON();
  patch_Notebook_to_markdown();
  patch_MarkdownCell_unrender();
  patch_MarkdownCell_render();
  render_e2x_cells();
}
