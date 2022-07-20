define(["./extended_cell"], function (extended_cell) {
  "use strict";

  let ExtendedCell = extended_cell.ExtendedCell;

  class PDFCell extends ExtendedCell {
    constructor(cell) {
      super(cell, "pdf");
    }

    render() {
      this.cell.unsafe_render();
      this.render_grader_settings();
      this.cell.keyboard_manager.disable();
    }
  }

  return {
    PDFCell: PDFCell,
  };
});
