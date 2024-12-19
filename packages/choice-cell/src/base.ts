import { MarkdownCell } from '@jupyterlab/cells';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IE2xCell, E2xCell } from '@e2xgrader/cell-core';

export interface IChoiceCell extends IE2xCell {
  setChoices: (choices: string[]) => void;
  getChoices: () => string[];
}

export abstract class ChoiceCell extends E2xCell implements IChoiceCell {
  choice_field: string;

  constructor(
    cell: MarkdownCell,
    type: string,
    settings: ISettingRegistry.ISettings,
    options: object = {}
  ) {
    super(cell, type, settings, options);
    this.choice_field = 'choice';
  }

  getChoices(): string[] {
    return this.model.getE2xgraderMetadataKey(this.choice_field, []);
  }

  setChoices(choices: any): void {
    this.model.setE2xgraderMetadataKey(this.choice_field, choices);
  }
}
