import { load_help_tab } from "@e2xgrader/help-tab";
import { add_tab_link } from "./tab-link";

export function load_ipython_extension() {
  load_help_tab();
  add_tab_link("Authoring", "e2x", "authoring", "app");
}
