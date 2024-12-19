import { Dialog, showDialog } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { CommandRegistry } from '@lumino/commands';

export namespace AuthoringDialogs {
  class InsertQuestionDialogBody extends Widget {
    constructor(initialName: string) {
      super();
      this.addQuestionNameInput(initialName);
      this.addPointsInput();
    }

    private addQuestionNameInput(initialName: string): void {
      // Create label and input and also add an id
      const label = document.createElement('label');
      label.textContent = 'Question name';
      label.htmlFor = 'question-name';
      const input = document.createElement('input');
      input.id = 'question-name';
      input.value = initialName;
      this.node.appendChild(label);
      this.node.appendChild(input);
    }

    private addPointsInput(): void {
      // Create label and input and also add an id
      const label = document.createElement('label');
      label.textContent = 'Points';
      label.htmlFor = 'points';
      const input = document.createElement('input');
      input.type = 'number';
      // Only positive numbers
      input.min = '0';
      input.id = 'points';
      this.node.appendChild(label);
      this.node.appendChild(input);
    }

    getValue(): { name: string; points: number } {
      const name = (
        this.node.querySelector('#question-name') as HTMLInputElement
      ).value;
      const points = Number(
        (this.node.querySelector('#points') as HTMLInputElement).value
      );
      return { name, points };
    }
  }

  export function createInsertQuestionDialog(
    commands: CommandRegistry,
    question_type: string,
    initial_name: string
  ): void {
    const body = new InsertQuestionDialogBody(initial_name);

    showDialog({
      title: `Insert question: ${question_type}`,
      body,
      buttons: [Dialog.okButton(), Dialog.cancelButton()]
    }).then(result => {
      if (result.button.accept) {
        const value = body.getValue();
        commands.execute('e2xgrader:insert-question', {
          preset_name: question_type,
          grade_id: value.name,
          points: value.points
        });
      }
    });
  }
}
