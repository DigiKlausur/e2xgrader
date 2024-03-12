import Jupyter from "base/js/namespace";
import { urlJoin, requests } from "@e2xgrader/api";

/**
 * Adds the username to the login widget.
 */
export function add_username() {
  const notebookBaseUrl = Jupyter.notebook
    ? Jupyter.notebook.base_url
    : Jupyter.notebook_list.base_url;

  requests.get(urlJoin(notebookBaseUrl, "nbgrader_username")).then((data) => {
    const usernameSpan = document.createElement("span");
    usernameSpan.id = "username_span";
    usernameSpan.textContent = data.username;
    usernameSpan.style.fontSize = "1.5em";

    const loginWidget = document.getElementById("login_widget");
    loginWidget.parentNode.insertBefore(usernameSpan, loginWidget);
  });
}
