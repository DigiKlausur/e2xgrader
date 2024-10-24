import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { INotebookTracker } from '@jupyterlab/notebook';

import { MarkdownCell } from '@jupyterlab/cells';
import { e2xCellFactory, e2xCellUtils } from '@e2xgrader/cells';
import Settings from '@e2xgrader/settings';

const PLUGIN_ID = '@e2xgrader/cell-extension:plugin';

function listenToMetadataChanges(cell: MarkdownCell) {
  const model = cell.model;
  // Problem: This does not seem to be triggered when a metadata key is removed via the metadata editor
  // However, it is triggered when the metadata is changed via deleteMetadata
  model.metadataChanged.connect((_: any, args: any) => {
    console.log(
      'Did the e2xgrader cell type change?',
      e2xCellUtils.hasE2xGraderCellTypeChanged(args)
    );
    if (e2xCellUtils.hasE2xGraderCellTypeChanged(args)) {
      e2xCellUtils.forceRender(cell);
    }
  });
}

function listenToRenderChanges(cell: MarkdownCell) {
  cell.renderedChanged.connect((_: any, isRendered: boolean) => {
    // Skip if the cell is not rendered
    if (!isRendered) {
      return;
    }
    Settings.getInstance(PLUGIN_ID).then(
      (settings: ISettingRegistry.ISettings) => {
        console.log('Settings loaded:', settings);
        const e2xCell = e2xCellFactory(cell, settings);
        if (e2xCell) {
          e2xCell.onCellRendered();
        }
      }
    );
  });
  e2xCellUtils.forceRender(cell);
}

/**
 * Initialization data for the e2xgrader_cells extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab for displaying custom e2xgrader cells',
  autoStart: true,
  requires: [INotebookTracker, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    notebooks: INotebookTracker,
    settings: ISettingRegistry
  ) => {
    Settings.initialize(PLUGIN_ID, settings);
    console.log('JupyterLab extension e2xgrader_cells is activated!');

    notebooks.widgetAdded.connect((_, notebookPanel) => {
      const notebook = notebookPanel.content;

      if (!notebook?.model) {
        return;
      }

      notebook.model.cells.changed.connect((_, args) => {
        // Skip if the cell is not being added
        if (args.type !== 'add') {
          return;
        }

        for (const cell of args.newValues) {
          // Skip non markdown cells
          if (!cell.type || cell.type !== 'markdown') {
            continue;
          }
          // Find the widget by matching ids
          const cellWidget = notebook.widgets.find(
            widget => widget.model.id === cell.id
          );
          if (!cellWidget) {
            console.error('Cell widget not found');
            continue;
          }

          const markdownCellWidget = cellWidget as MarkdownCell;

          listenToMetadataChanges(markdownCellWidget);
          listenToRenderChanges(markdownCellWidget);

          // Rerender e2xgrader cells
          e2xCellUtils.forceRender(markdownCellWidget);
        }
      });
    });
  }
};

export default plugin;
