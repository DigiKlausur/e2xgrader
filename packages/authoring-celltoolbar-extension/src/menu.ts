import { Menu, MenuBar } from '@lumino/widgets';
import { CommandRegistry } from '@lumino/commands';
import {
  NotebookPanel,
  INotebookTracker,
  NotebookModel
} from '@jupyterlab/notebook';
import { IToolbarWidgetRegistry } from '@jupyterlab/apputils';
import { AuthoringAPI } from './api';
import { commandIDs } from './commands';
import { GradingCellModel } from '@e2xgrader/cell-core';
import { SharedCell, createStandaloneCell } from '@jupyter/ydoc';

export namespace AuthoringMenubar {
  export function registerAuthoringToolbarFactory(
    commands: CommandRegistry,
    toolbarRegistry: IToolbarWidgetRegistry
  ): void {
    toolbarRegistry.addFactory<NotebookPanel>(
      'Notebook',
      'e2x-switcher',
      Private.createAuthoringToolbarFactory(commands)
    );
  }

  namespace Private {
    export function createAuthoringToolbarFactory(
      commands: CommandRegistry
    ): (panel: NotebookPanel) => MenuBar {
      const switcher = new Menu({ commands });
      const overflowOptions = {
        overflowMenuOptions: {
          isVisible: false
        }
      };

      AuthoringAPI.listQuestionPresets().then((presets: any) => {
        presets.data.forEach((preset: string) => {
          switcher.addItem({
            args: { label: preset },
            command: commandIDs.openQuestionDialog
          });
        });
      });

      return (_panel: NotebookPanel) => {
        const menubar = new MenuBar(overflowOptions);
        menubar.addClass('e2x-menubar');
        switcher.title.label = 'Insert Question';
        menubar.addMenu(switcher);
        return menubar;
      };
    }
  }
}

export namespace AuthoringMenubarUtils {
  export function getValidName(name: string): string {
    const alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const alphabet_lower = 'abcdefghijklmnopqrstuvwxyz';
    const numbers = '0123456789';
    const special = '_';
    const valid_chars = alphabet_upper + alphabet_lower + numbers + special;
    // Replace invalid characters with '_'
    let valid_name = '';
    for (const element of name) {
      if (valid_chars.includes(element)) {
        valid_name += element;
      } else {
        valid_name += '_';
      }
    }
    return valid_name;
  }

  export function getGradeIds(notebook: NotebookModel): string[] {
    const grade_ids: string[] = [];
    notebook.sharedModel.cells.forEach(cell => {
      const gradingCell = new GradingCellModel(cell);
      const grade_id = gradingCell.gradeId;
      if (grade_id) {
        grade_ids.push(grade_id);
      }
    });
    return grade_ids;
  }

  export function getTaskName(
    notebookTracker: INotebookTracker
  ): string | undefined {
    // First find the name of the notebook and split the .ipynb extension
    const file_name =
      notebookTracker.currentWidget?.context.contentsModel?.name;
    if (!file_name) {
      return undefined;
    }
    const nb_name = getValidName(file_name.split('.ipynb')[0]);
    const grade_ids = getGradeIds(
      notebookTracker.currentWidget?.model as NotebookModel
    );
    // Now we create a task name by adding an underscore and a letter.
    // If the task name already exists, we increment the letter
    let task_name = nb_name + '_A';
    let i = 0;
    while (grade_ids.includes(task_name)) {
      i++;
      task_name = nb_name + '_' + String.fromCharCode(65 + i);
    }
    return task_name;
  }

  export function setTaskIds(
    cells: SharedCell.Cell[],
    task_name: string,
    points: number
  ): SharedCell.Cell[] {
    const new_cells: SharedCell.Cell[] = [];
    let n_read_only = 0;
    let n_tests = 0;
    for (const cell of cells) {
      const gradingCell = new GradingCellModel(createStandaloneCell(cell));
      if (!gradingCell.isNbgraderCell) {
        new_cells.push(cell);
        continue;
      }
      if (gradingCell.isGrade) {
        gradingCell.points = points;
      }
      if (gradingCell.isSolution) {
        gradingCell.gradeId = task_name;
      } else if (gradingCell.isAutograderTest) {
        gradingCell.gradeId = `test_${n_tests}_${task_name}`;
        n_tests++;
      } else if (gradingCell.isDescription) {
        gradingCell.gradeId = `${task_name}_description${n_read_only}`;
        n_read_only++;
      }

      new_cells.push(gradingCell.toJSON());
    }
    return new_cells;
  }

  export function insertQuestionPreset(
    notebookModel: NotebookModel,
    cells: SharedCell.Cell[],
    grade_id: string,
    points: number
  ) {
    const new_cells = setTaskIds(cells, grade_id, points);
    new_cells.forEach(cellData => {
      notebookModel.sharedModel.addCell({
        cell_type: cellData.cell_type,
        metadata: cellData.metadata,
        source: cellData.source
      });
    });
  }
}
