import $ from "jquery";
import Jupyter from "base/js/namespace";
import { urlJoin, requests } from "@e2xgrader/api";

function createHelpLink(href, text, target = "_blank") {
  return $("<a/>").attr("href", href).attr("target", target).text(text);
}

function createListItemWithLink(href, text) {
  return $("<li/>").append(createHelpLink(href, text));
}

function createHelpTab() {
  const body = $("<div/>").attr("id", "e2xhelp").addClass("tab-pane");
  const resources = $("<div/>").attr("id", "resources");
  resources.append($("<h4/>").append("Resources"));
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
        .on("click", function (_event) {
          window.history.pushState(null, null, "#e2xhelp");
          requests
            .get(urlJoin(Jupyter.notebook_list.base_url, "e2x/help/api/files"))
            .then((data) => {
              let additional_links = $("#additional-links");
              additional_links.empty();
              let links = $("<ul/>");
              data.forEach(function (entry) {
                links.append(
                  createListItemWithLink(
                    urlJoin(
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
