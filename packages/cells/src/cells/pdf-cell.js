import { E2xCell } from "./base";

export class PDFCell extends E2xCell {
  constructor(cell) {
    super(cell, "pdf");
  }

  render() {
    this.cell.unsafe_render();
    this.render_grader_settings();
    this.cell.keyboard_manager.disable();
  }
}
