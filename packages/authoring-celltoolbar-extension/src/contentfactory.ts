import { ICellHeader, Cell } from '@jupyterlab/cells';
import { NotebookPanel } from '@jupyterlab/notebook';
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IEditorServices } from '@jupyterlab/codeeditor';
import { AuthoringCellToolbar } from './toolbar';
import { ICellRegistry } from '@e2xgrader/cell-core';

const PLUGIN_ID = '@e2xgrader/authoring-celltoolbar-extension:cell-factory';

export class ContentFactoryWithAuthoringToolbar extends NotebookPanel.ContentFactory {
  cellRegistry: ICellRegistry;
  constructor(
    options: Cell.ContentFactory.IOptions,
    cellRegistry: ICellRegistry
  ) {
    super(options);
    this.cellRegistry = cellRegistry;
  }
  createCellHeader(): ICellHeader {
    return AuthoringCellToolbar.createAuthoringToolbar(this.cellRegistry);
  }
}

export const cellFactoryExtension: JupyterFrontEndPlugin<NotebookPanel.IContentFactory> =
  {
    id: PLUGIN_ID,
    autoStart: true,
    requires: [IEditorServices, ICellRegistry],
    provides: NotebookPanel.IContentFactory,
    activate: (
      _app: JupyterFrontEnd,
      editorServices: IEditorServices,
      cellRegistry: ICellRegistry
    ): NotebookPanel.IContentFactory => {
      console.log('Activating cell factory extension');
      const editorFactory = editorServices.factoryService.newInlineEditor;
      return new ContentFactoryWithAuthoringToolbar(
        { editorFactory },
        cellRegistry
      );
    }
  };
