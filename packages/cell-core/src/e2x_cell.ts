import { MarkdownCell } from '@jupyterlab/cells';
import { MimeModel } from '@jupyterlab/rendermime';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { RenderUtils } from './renderutils';
import { GradingCellModel } from './model';

export const E2X_GRADER_SETTINGS_CLASS = 'e2x_grader_options';
export const E2X_UNRENDER_BUTTON_CLASS = 'e2x_unrender';
export const E2X_BUTTON_CLASS = 'e2x_btn';

export namespace E2xGraderMetadata {
  export interface IE2xGraderMetadata {
    type: string;
    [key: string]: any;
  }

  export const E2XGRADER_METADATA_KEY = 'extended_cell';
}

export interface IE2xCell {
  cell: MarkdownCell;
  model: GradingCellModel;
  type: string;
  settings: ISettingRegistry.ISettings;
  options: object;
  onCellRendered: () => void;
  manipulateHTML: (html: Element) => void;
  renderGraderSettings: (html: Element) => void;
}

export abstract class E2xCell implements IE2xCell {
  private readonly _cell: MarkdownCell;
  model: GradingCellModel;
  type: string;
  options: object;
  settings: ISettingRegistry.ISettings;
  editMode: boolean;

  constructor(
    cell: MarkdownCell,
    type: string,
    settings: ISettingRegistry.ISettings,
    options: object = {}
  ) {
    this._cell = cell;
    this.model = new GradingCellModel(cell.model.sharedModel);
    this.type = type;
    this.settings = settings;
    this.options = options;
    // Make sure cells can not be unrendered
    this._cell.showEditorForReadOnly = false;
    this.editMode = true;

    this.onSettingsChanged(settings);
    settings.changed.connect(this.onSettingsChanged, this);
  }

  get cell(): MarkdownCell {
    return this._cell;
  }

  private onSettingsChanged(settings: ISettingRegistry.ISettings): void {
    const newEditMode = settings.get('edit_mode').composite as boolean;
    if (newEditMode !== this.editMode) {
      this.editMode = newEditMode;
      if (this.cell.rendered) {
        this.onCellRendered();
      }
    }
  }

  onCellRendered() {
    this.cell.readOnly = true;
    // Force a clean render of the cell.
    // This is necessary because the cell will not be rendered again if the source is the same.
    this.cell.renderer
      .renderModel(
        new MimeModel({
          data: { 'text/markdown': this.cell.model.sharedModel.getSource() }
        })
      )
      .then(() => {
        this.render();
      })
      .catch(error => {
        console.error('Error rendering cell', error);
      });
  }

  render(): void {
    RenderUtils.getHTML(this.cell).then(html => {
      this.manipulateHTML(html).then(() => {
        if (this.editMode) {
          this.renderGraderSettings(html);
        }
      });
    });
  }

  abstract manipulateHTML(html: Element): Promise<void>;

  renderGraderSettings(html: Element): void {
    const container = document.createElement('div');
    container.className = E2X_GRADER_SETTINGS_CLASS;
    const unrenderButton = document.createElement('button');
    unrenderButton.className =
      E2X_UNRENDER_BUTTON_CLASS + ' ' + E2X_BUTTON_CLASS;
    unrenderButton.textContent = 'Edit Cell';
    unrenderButton.onclick = () => {
      this.cell.readOnly = false;
      this.cell.rendered = false;
    };
    container.appendChild(document.createElement('hr'));
    container.appendChild(unrenderButton);
    const optionContainer = document.createElement('div');
    optionContainer.className = 'e2x-option-container';
    container.appendChild(document.createElement('br'));
    container.appendChild(optionContainer);
    html.appendChild(container);
  }
}
