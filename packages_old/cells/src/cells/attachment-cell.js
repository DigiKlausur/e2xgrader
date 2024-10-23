import $ from "jquery";
import { AttachmentModel } from "../utils/attachment-model";
import { AttachmentGallery } from "../utils/attachment-view";
import { E2xCell } from "./base";

class AttachmentCellModel extends AttachmentModel {
  postSaveHook() {
    let cleaned = this.cell.get_text().replace(this.imagePattern, "");
    cleaned = cleaned.replace(this.infoPattern, "");
    let n_attachments = Object.keys(this.attachments).length;
    cleaned += "\n### You uploaded " + n_attachments + " attachments.\n\n";
    this.cell.set_text(cleaned);
    this.cell.unrender_force();
    this.cell.render();
  }

  getName(name, type) {
    let current_name = name + "." + type;
    let counter = 0;
    while (current_name in this.attachments) {
      counter += 1;
      current_name = name + "_" + counter + "." + type;
    }
    return current_name;
  }
}

export class AttachmentCell extends E2xCell {
  constructor(cell) {
    super(cell, "attachments");
    this.model = new AttachmentCellModel(cell);
    this.view = new AttachmentGallery(cell, this.model);
  }

  get_attachment_button() {
    let that = this;
    return $("<button>")
      .attr("type", "button")
      .addClass("edit_attachments btn-e2x")
      .on("click", function () {
        that.view.open();
      })
      .append("Add Files / Images");
  }

  render() {
    this.cell.render_force();
    let html = $(this.cell.element).find(".rendered_html");
    if (html.find(".edit_attachments").length < 1) {
      html.append(this.get_attachment_button());
    }
    this.render_grader_settings();
  }
}
