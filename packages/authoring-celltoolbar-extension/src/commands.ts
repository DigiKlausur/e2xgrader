import { CommandRegistry } from '@lumino/commands';
import { INotebookTracker, NotebookModel } from '@jupyterlab/notebook';
import { AuthoringDialogs } from './dialogs';
import { AuthoringMenubarUtils } from './menu';
import { AuthoringAPI } from './api';

export const commandIDs = {
  openQuestionDialog: 'e2xgrader:open-question-dialog',
  insertQuestion: 'e2xgrader:insert-question'
};

export function registerCommands(
  commands: CommandRegistry,
  notebookTracker: INotebookTracker
): void {
  registerOpenQuestionDialogCommand(commands, notebookTracker);
  registerInsertQuestionCommand(commands, notebookTracker);
}

function registerOpenQuestionDialogCommand(
  commands: CommandRegistry,
  notebookTracker: INotebookTracker
): void {
  commands.addCommand(commandIDs.openQuestionDialog, {
    label: (args: any) => args['label'] || 'Insert question',
    execute: args => {
      const taskName = AuthoringMenubarUtils.getTaskName(notebookTracker);
      if (args['label'] && taskName) {
        console.log('Inserting question', args['label']);
        AuthoringDialogs.createInsertQuestionDialog(
          commands,
          args['label'] as string,
          taskName
        );
      }
    }
  });
}

function registerInsertQuestionCommand(
  commands: CommandRegistry,
  notebookTracker: INotebookTracker
): void {
  commands.addCommand(commandIDs.insertQuestion, {
    label: 'Insert question',
    execute: args => {
      const { preset_name, grade_id, points } = args as {
        preset_name: string;
        grade_id: string;
        points: number;
      };
      AuthoringAPI.getQuestionPreset(preset_name).then((preset: any) => {
        const nbModel = notebookTracker.currentWidget?.model as NotebookModel;
        AuthoringMenubarUtils.insertQuestionPreset(
          nbModel,
          preset.data,
          grade_id,
          points
        );
      });
    }
  });
}
