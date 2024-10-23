import $ from "jquery";
import "./menubar.css";

export class Menubar {
  constructor() {
    this.element = $("<div/>")
      .attr("id", "e2x-menubar")
      .append($("<span/>").text("e²x").addClass("e2x-badge"));
  }

  hide_maintoolbar() {
    $("#maintoolbar-container").hide();
  }

  add_divider() {
    this.element.append($("<div/>").addClass("e2x-divider").append("&nbsp;"));
  }

  add_spacer() {
    this.element.append($("<div/>").addClass("e2x-spacer"));
  }

  add_save_button() {
    this.element.append($("#save-notbook"));
  }

  add_run_controls() {
    this.element.append($("#run_int"));
  }

  add_button(label, callback) {
    this.element.append(
      $("<div/>").addClass("e2x-button").on("click", callback).append(label),
    );
  }

  add_link(label, href, target = "_blank") {
    this.element.append(
      $("<a/>")
        .addClass("e2x-button")
        .attr("href", href)
        .attr("target", target)
        .append(label),
    );
  }

  add_dropdown(id, label, items) {
    let dropdown = $("<div/>").addClass("e2x-dropdown");
    dropdown.append(
      $("<span/>")
        .attr("id", id)
        .append($("<a/>").append(label))
        .addClass("e2x-button"),
    );

    let menuitems = $("<ul/>").addClass("e2x-dropdown-content");

    for (const item of items) {
      let li = $("<li/>")
        .addClass("e2x-dropdown-item")
        .append($("<a/>").append(item.label));
      li.on("click", item.callback);
      menuitems.append(li);
    }
    this.element.append(dropdown.append(menuitems));
  }

  activate() {
    this.hide_maintoolbar();
    this.element.insertAfter($("#maintoolbar-container"));
  }
}
