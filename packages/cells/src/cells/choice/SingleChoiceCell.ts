import { MarkdownCell } from '@jupyterlab/cells';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getE2xGraderField } from '../utils/cellUtils';
import ChoiceCell from './ChoiceCell';

export const E2X_SINGLECHOICE_CELL_TYPE = 'singlechoice';

export default class SingleChoiceCell extends ChoiceCell {
  constructor(
    cell: MarkdownCell,
    settings: ISettingRegistry.ISettings,
    options: object = {}
  ) {
    super(cell, E2X_SINGLECHOICE_CELL_TYPE, settings, options);
  }

  getChoice(): string {
    return getE2xGraderField(this.cell, this.choice_field, '');
  }

  createChoiceElement(
    name: string,
    value: string,
    selected: boolean
  ): HTMLInputElement {
    const choice = document.createElement('input');
    choice.type = 'radio';
    choice.name = name;
    choice.value = value;
    choice.checked = selected;
    choice.onchange = event => {
      const elem = event.target as HTMLInputElement;
      this.setChoices(elem.value);
    };
    return choice;
  }

  manipulateHTML(html: Element): Promise<void> {
    const lists = html.querySelectorAll('ul');

    if (lists.length === 0) {
      return Promise.resolve();
    }

    // We only care about the first list
    const list = lists[0];
    const form = document.createElement('form');
    form.className = 'e2xgrader-singlechoice-form';
    const items = list.querySelectorAll('li');
    const choice = this.getChoice();
    if (choice !== '' && parseInt(choice) >= items.length) {
      this.setChoices('');
    }
    items.forEach((item, idx) => {
      const radioButton = this.createChoiceElement(
        'choice',
        idx.toString(),
        choice === idx.toString()
      );
      const label = document.createElement('label');
      label.innerHTML = item.innerHTML;
      form.appendChild(radioButton);
      form.appendChild(label);
      form.appendChild(document.createElement('br'));
    });
    list.replaceWith(form);
    return Promise.resolve();
  }
}
