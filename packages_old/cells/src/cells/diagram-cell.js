import { E2xCell } from "./base";
import { AttachmentModel } from "../utils/attachment-model";
import DiagramEditor from "../utils/diagram-editor";

class DiagramCellModel extends AttachmentModel {
  postSaveHook() {
    this.cell.unrender_force();
    this.cell.render();
  }
}

export class DiagramCell extends E2xCell {
  constructor(cell) {
    super(cell, "diagram", {
      replace_diagram: {
        type: "checkbox",
        text: "Replace this diagram with an empty diagram in the student version",
        value: true,
      },
    });
    this.model = new DiagramCellModel(cell);
    this.initialize();
  }

  initialize() {
    // Check if we already have an attachment, if not create it
    this.model.load();
    if (!this.model.hasAttachment("diagram.png")) {
      this.model.setAttachment(
        "diagram.png",
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAYAAABxLb1rAAAABHNCSVQICAgIfAhkiAAAAylJREFUeJzt1DEBACAMwDDAv+chY0cTBb16Z2YOQNDbDgDYYoBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZH97eBdx+cY1yAAAAAElFTkSuQmCC",
      );
    }
  }

  render() {
    let that = this;

    let attachment_string = "![diagram](attachment:diagram.png)";
    let attachment_comment = "<!-- Display the diagram attachment -->";
    if (this.cell.get_text().indexOf(attachment_string) == -1) {
      this.cell.set_text(
        [this.cell.get_text(), attachment_comment, attachment_string].join(
          "\n",
        ),
      );
    }

    this.cell.render_force();

    let html = $(this.cell.element).find(".rendered_html");

    let img = html.find("img");
    img.addClass("diagram-img");

    // Remove old button if there is any
    $(html).find(".btn-diagram").remove();
    let button = $("<button/>")
      .append("Edit Diagram")
      .addClass("btn-e2x btn-diagram");

    button.on("click", async () => {
      try {
        await DiagramEditor.editDiagram(that, img[0]);
      } catch (error) {
        console.error("Failed to load DiagramEditor:", error);
      }
    });

    html.append(img);
    html.append(button);
    this.render_grader_settings();
  }
}
