import "./exam-tree.css";
import { load_help_tab } from "@e2xgrader/help-tab";
import { username } from "@e2xgrader/utils";

export function load_ipython_extension() {
  load_help_tab();
  username.add_username();
}
