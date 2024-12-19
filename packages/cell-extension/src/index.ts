import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker, Notebook } from '@jupyterlab/notebook';
import { MarkdownCell } from '@jupyterlab/cells';

import { RenderUtils, ICellRegistry } from '@e2xgrader/cell-core';
import {
  MultipleChoiceCell,
  E2X_MULTIPLECHOICE_CELL_TYPE,
  E2X_MULTIPLECHOICE_CELL_LABEL,
  SingleChoiceCell,
  E2X_SINGLECHOICE_CELL_TYPE,
  E2X_SINGLECHOICE_CELL_LABEL
} from '@e2xgrader/choice-cell';
import {
  DiagramCell,
  E2X_DIAGRAM_CELL_TYPE,
  E2X_DIAGRAM_CELL_LABEL
} from '@e2xgrader/diagram-cell';

import { CellFactory } from './factory';
import { CellHandlers } from './cellHandlers';

const PLUGIN_ID = '@e2xgrader/cell-extension:plugin';
const CELL_TYPE_MARKDOWN = 'markdown';
const CELL_CHANGE_TYPE_ADD = 'add';

/**
 * Handles changes to the cells in a notebook. Specifically, it listens for the addition of new cells
 * and performs specific actions if the new cell is a markdown cell.
 *
 * @param notebook - The notebook instance whose cells are being monitored.
 * @param cellRegistry - The registry that keeps track of cell types and their handlers.
 *
 * The function performs the following actions when a new markdown cell is added:
 * - Finds the corresponding cell widget in the notebook.
 * - Listens to metadata changes on the markdown cell.
 * - Listens to render changes on the markdown cell.
 * - Listens for new cell registrations.
 * - Forces a render of the markdown cell to ensure it is displayed correctly.
 */
function handleCellsChanged(notebook: Notebook, cellRegistry: ICellRegistry) {
  if (!notebook?.model) {
    return;
  }
  notebook.model.cells.changed.connect((_, args) => {
    if (args.type !== CELL_CHANGE_TYPE_ADD) {
      return;
    }

    for (const cell of args.newValues) {
      if (!cell.type || cell.type !== CELL_TYPE_MARKDOWN) {
        continue;
      }

      const cellWidget = notebook.widgets.find(
        widget => widget.model.id === cell.id
      );
      if (!cellWidget) {
        console.error('Cell widget not found');
        continue;
      }

      const markdownCellWidget = cellWidget as MarkdownCell;

      CellHandlers.listenToMetadataChanges(markdownCellWidget);
      CellHandlers.listenToRenderChanges(markdownCellWidget);
      CellHandlers.listenToNewCellRegistered(markdownCellWidget, cellRegistry);

      // Rerender once to make sure the e2xgrader cell is rendered correctly
      RenderUtils.forceRender(markdownCellWidget);
    }
  });
}

/**
 * Initialization data for the e2xgrader_cells extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab for displaying custom e2xgrader cells',
  autoStart: true,
  requires: [INotebookTracker, ISettingRegistry, ICellRegistry],
  activate: async (
    _app: JupyterFrontEnd,
    notebooks: INotebookTracker,
    settings: ISettingRegistry,
    cellRegistry: ICellRegistry
  ) => {
    console.log('JupyterLab extension e2xgrader_cells is activated!');

    cellRegistry.registerCellType(
      E2X_MULTIPLECHOICE_CELL_TYPE,
      E2X_MULTIPLECHOICE_CELL_LABEL,
      MultipleChoiceCell
    );
    cellRegistry.registerCellType(
      E2X_SINGLECHOICE_CELL_TYPE,
      E2X_SINGLECHOICE_CELL_LABEL,
      SingleChoiceCell
    );
    cellRegistry.registerCellType(
      E2X_DIAGRAM_CELL_TYPE,
      E2X_DIAGRAM_CELL_LABEL,
      DiagramCell
    );

    try {
      const pluginSettings = await settings.load(PLUGIN_ID);
      CellFactory.initialize(cellRegistry, pluginSettings);
    } catch (error) {
      console.error(
        `Failed to load settings for plugin ID ${PLUGIN_ID}:`,
        error
      );
    }

    notebooks.widgetAdded.connect((_, notebookPanel) => {
      const notebook = notebookPanel.content;
      handleCellsChanged(notebook, cellRegistry);
    });
  }
};

export default plugin;
