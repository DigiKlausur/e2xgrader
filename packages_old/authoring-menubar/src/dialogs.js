import $ from "jquery";
import Jupyter from "base/js/namespace";
import dialog from "base/js/dialog";
import { get_valid_task_name } from "./utils";

function get_tags() {
  let nb_metadata = Jupyter.notebook.metadata;
  if (
    nb_metadata.hasOwnProperty("nbassignment") &&
    nb_metadata.nbassignment.hasOwnProperty("tags")
  ) {
    return nb_metadata.nbassignment.tags.join(", ");
  }
  return [];
}

function add_tags(tags) {
  let tag_array = [];
  if (tags.trim().length > 0) {
    tag_array = tags.split(",");
    for (let i = 0; i < tag_array.length; i++) {
      tag_array[i] = tag_array[i].trim();
    }
  }
  let metadata = Jupyter.notebook.metadata;
  if (!metadata.hasOwnProperty("nbassignment")) {
    metadata["nbassignment"] = {
      tags: tag_array,
    };
  } else {
    metadata.nbassignment["tags"] = tag_array;
  }
}

export function manage_tags() {
  let body = $("<div/>").addClass("e2x-dialog");
  let table = $("<table/>");

  let name = $("<tr/>");
  name.append(
    $("<td/>").append($("<span/>").text("Tags: (separate by comma)")),
  );

  table.append(name);

  let tags = $("<span/>");
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
}

export function insert_question_preset_dialog(preset_name, callback) {
  let table = $("<table/>").addClass("e2xtable");

  let nameRow = $("<tr/>")
    .append($("<td/>").append($("<span/>").text("Name:")))
    .append(
      $("<td/>")
        .addClass("column2")
        .append(
          $("<input/>")
            .attr("type", "text")
            .attr("id", "taskname")
            .val(get_valid_task_name()),
        ),
    );

  let pointRow = $("<tr/>")
    .append($("<td/>").append($("<span/>").text("Points:")))
    .append(
      $("<td/>")
        .addClass("column2")
        .append(
          $("<input/>")
            .attr("type", "number")
            .attr("id", "points")
            .attr("min", "0")
            .val(0),
        ),
    );

  let body = $("<div/>").append(table.append(nameRow).append(pointRow));
  dialog.modal({
    keyboard_manager: Jupyter.keyboard_manager,
    title: `Insert Question - ${preset_name}`,
    body: body,
    buttons: {
      OK: {
        click: () => callback($("#taskname").val(), Number($("#points").val())),
      },
      Cancel: {},
    },
  });
}
