import {
  AttachmentModel,
  E2xCell,
  E2X_BUTTON_CLASS,
  RenderUtils
} from '@e2xgrader/cell-core';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IDiagramCell, Base64ImageString } from './interfaces';
import { startDiagramEditor } from './diagram-editor';

export const E2X_DIAGRAM_CLASS = 'e2x-diagram';

export const E2X_DIAGRAM_CELL_TYPE = 'diagram';

export class DiagramCell extends E2xCell implements IDiagramCell {
  diagram_file_name: string;
  model: AttachmentModel;

  constructor(cell: any, settings: ISettingRegistry.ISettings) {
    super(cell, E2X_DIAGRAM_CELL_TYPE, settings, {
      properties: {
        replace_diagram: {
          type: 'boolean',
          title:
            'Replace this diagram with an empty diagram in the student version',
          default: false,
          required: true
        }
      }
    });
    this.diagram_file_name = 'diagram.png';
    this.model = new AttachmentModel(this);
    this.initialize();
  }

  initialize(): void {
    this.model.load();
    if (!this.model.hasAttachment(this.diagram_file_name)) {
      // Create a blank image attachment
      const canvas = document.createElement('canvas');
      canvas.width = 320;
      canvas.height = 240;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const blankImageBase64 = canvas.toDataURL('image/png');
        this.model.setAttachment('diagram.png', blankImageBase64);
      }
      canvas.remove();
    }
  }

  updateDiagramAttachment(attachment: Base64ImageString): void {
    this.model.setAttachment(this.diagram_file_name, attachment);
    RenderUtils.forceRender(this.cell);
    this.onCellRendered();
  }

  updateDiagram(diagramImage: HTMLImageElement): void {
    const diagramAttachment = this.model.getAttachment(this.diagram_file_name);
    diagramImage.src =
      'data:' + diagramAttachment.type + ';base64,' + diagramAttachment.data;
  }

  createDiagramEditButton(diagramImage: HTMLImageElement): HTMLButtonElement {
    const diagramEditButton = document.createElement('button');
    diagramEditButton.innerHTML = 'Edit Diagram';
    diagramEditButton.className = E2X_BUTTON_CLASS;
    diagramEditButton.onclick = () => {
      startDiagramEditor(this, diagramImage);
    };
    return diagramEditButton;
  }

  async manipulateHTML(html: Element): Promise<void> {
    const attachment_string = `![diagram](attachment:${this.diagram_file_name})`;
    const attachment_comment = '<!-- Display the diagram attachment -->';
    if (
      this.cell.model.sharedModel.getSource().indexOf(attachment_string) === -1
    ) {
      this.cell.model.sharedModel.setSource(
        this.cell.model.sharedModel.getSource() +
          '\n' +
          attachment_string +
          '\n' +
          attachment_comment
      );
    }

    // Find the diagram image in the html which should have the alt text 'diagram'
    const waitForImage = (
      html: Element,
      timeout: number
    ): Promise<HTMLImageElement> => {
      return new Promise((resolve, reject) => {
        const interval = 100;
        let elapsedTime = 0;

        const checkForImage = () => {
          const diagramImage: HTMLImageElement | null =
            html.querySelector('img[alt="diagram"]');
          if (diagramImage) {
            resolve(diagramImage);
          } else if (elapsedTime >= timeout) {
            reject(new Error('Image not found within timeout period'));
          } else {
            elapsedTime += interval;
            setTimeout(checkForImage, interval);
          }
        };

        checkForImage();
      });
    };

    try {
      const diagramImage_1 = await waitForImage(html, 5000);
      this.updateDiagram(diagramImage_1);
      diagramImage_1.className = E2X_DIAGRAM_CLASS;
      const diagramEditButton = this.createDiagramEditButton(diagramImage_1);
      // Remove all existing diagram buttons, by class name
      html.querySelectorAll(`.${E2X_BUTTON_CLASS}`).forEach(button => {
        button.remove();
      });
      html.appendChild(diagramEditButton);
    } catch (error) {
      console.error(error);
    }
  }
}
