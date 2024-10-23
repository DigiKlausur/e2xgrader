import { MultiplechoiceCell, SinglechoiceCell } from "./choice-cell";
import { PDFCell } from "./pdf-cell";
import { DiagramCell } from "./diagram-cell";
import { AttachmentCell } from "./attachment-cell";

export const cells = {
  multiplechoice: MultiplechoiceCell,
  singlechoice: SinglechoiceCell,
  pdf: PDFCell,
  attachments: AttachmentCell,
  diagram: DiagramCell,
};
