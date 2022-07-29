define([
  "jquery",
  "./extended_cell",
  "./attachment_view",
  "./attachment",
], function ($, extended_cell, attachment_view, attachment_model) {
  "use strict";

  let ExtendedCell = extended_cell.ExtendedCell;

  class AttachmentCell extends ExtendedCell {
    constructor(cell) {
      super(cell, "attachments");
      this.model = new attachment_model.AttachmentCellModel(cell);
      this.view = new attachment_view.AttachmentGallery(cell, this.model);
    }

    get_attachment_button() {
      let that = this;
      return $("<button>")
        .attr("type", "button")
        .addClass("edit_attachments btn-e2x")
        .click(function () {
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

  return {
    AttachmentCell: AttachmentCell,
  };
});
