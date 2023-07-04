import $ from "jquery";
import Jupyter from "base/js/namespace";
import utils from "base/js/utils";
import { BaseAPI } from "@e2xgrader/api";

function createHelpLink(href, text, target = "_blank") {
  return $("<a/>").attr("href", href).attr("target", target).text(text);
}

function createListItemWithLink(href, text) {
  return $("<li/>").append(createHelpLink(href, text));
}

function createHelpTabEntry(path, text) {
  const href = utils.url_path_join(Jupyter.notebook_list.base_url, path);
  return createListItemWithLink(href, text);
}

function createHelpTab() {
  const body = $("<div/>").attr("id", "e2xhelp").addClass("tab-pane");
  const help = $("<div/>").attr("id", "help");
  help.append($("<h4/>").append("General Help:"));
  const helpList = $("<ul/>");

  helpList.append(
    createHelpTabEntry("e2x/help/static/base/html/en", "E2X Help (English)")
  );
  helpList.append(
    createHelpTabEntry("e2x/help/static/base/html/de", "E2X Hilfe (Deutsch)")
  );
  body.append(help.append(helpList));

  const resources = $("<div/>").attr("id", "resources");
  resources.append($("<h4/>").append("Additional Resources"));
  resources.append($("<div/>").attr("id", "additional-links"));
  body.append(resources);
  return body;
}

export function load_help_tab() {
  if (!Jupyter.notebook_list) {
    return;
  }
  $(".tab-content").append(createHelpTab());
  $("#tabs").append(
    $("<li/>").append(
      $("<a/>")
        .attr("href", "#e2xhelp")
        .attr("data-toggle", "tab")
        .text("Help")
        .on("click", function (event) {
          window.history.pushState(null, null, "#e2xhelp");
          new BaseAPI()
            .get(
              utils.url_path_join(
                Jupyter.notebook_list.base_url,
                "e2x/help/api/files"
              )
            )
            .then((data) => {
              let additional_links = $("#additional-links");
              additional_links.empty();
              let links = $("<ul/>");
              data.forEach(function (entry) {
                links.append(
                  createListItemWithLink(
                    utils.url_path_join(
                      Jupyter.notebook_list.base_url,
                      "e2x/help/static/",
                      entry[1]
                    ),
                    entry[0]
                  )
                );
              });
              if (data.length > 0) {
                additional_links.append(links);
              } else {
                additional_links.append("There are no additional resources!");
              }
            });
        })
    )
  );
}
