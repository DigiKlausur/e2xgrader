import { load_assignment_list } from "@e2xgrader/assignment-list";
import { load_help_tab } from "@e2xgrader/help-tab";

export function load_ipython_extension() {
  load_assignment_list();
  load_help_tab();
}
