define(["jquery", "base/js/namespace", "base/js/dialog"], function (
  $,
  Jupyter,
  dialog,
  tasks
) {
  "use strict";

  function get_tags() {
    var metadata = Jupyter.notebook.metadata;
    if (
      metadata.hasOwnProperty("nbassignment") &&
      metadata.nbassignment.hasOwnProperty("tags")
    ) {
      return metadata.nbassignment.tags.join(", ");
    }
    return [];
  }

  function add_tags(tags) {
    var tag_array = [];
    if (tags.trim().length > 0) {
      tag_array = tags.split(",");
      for (var i = 0; i < tag_array.length; i++) {
        tag_array[i] = tag_array[i].trim();
      }
    }
    var metadata = Jupyter.notebook.metadata;
    if (!metadata.hasOwnProperty("nbassignment")) {
      metadata["nbassignment"] = {
        tags: tag_array,
      };
    } else {
      metadata.nbassignment["tags"] = tag_array;
    }
  }

  var manage_tags = function () {
    var body = $("<div/>").addClass("e2xdialog");
    var table = $("<table/>");

    var name = $("<tr/>");
    name.append(
      $("<td/>").append($("<span/>").text("Tags: (separate by comma)"))
    );

    table.append(name);

    var tags = $("<span/>");
    tags.append($("<textarea/>").attr("id", "tags").append(get_tags()));

    body.append(table);
    body.append(tags);

    dialog.modal({
      keyboard_manager: Jupyter.keyboard_manager,
      title: "Manage Tags",
      body: body,
      buttons: {
        OK: {
          click: function () {
            add_tags($("#tags").val());
          },
        },
        Cancel: {},
      },
    });
  };

  return {
    manage_tags: manage_tags,
  };
});
