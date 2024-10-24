import { MarkdownCell } from '@jupyterlab/cells';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

export interface IE2xCell {
  cell: MarkdownCell;
  type: string;
  settings: ISettingRegistry.ISettings;
  options: object;
  onCellRendered: () => void;
  manipulateHTML: (html: Element) => void;
  renderGraderSettings: (html: Element) => void;
}
