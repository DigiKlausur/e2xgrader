import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IToolbarWidgetRegistry } from '@jupyterlab/apputils';

import { cellFactoryExtension } from './contentfactory';
import { AuthoringCellToolbar } from './toolbar';
import { AuthoringMenubar } from './menu';
import { registerCommands } from './commands';

const PLUGIN_ID = '@e2xgrader/authoring-celltoolbar-extension:plugin';

const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension for authoring assignments',
  autoStart: true,
  requires: [INotebookTracker, ISettingRegistry, IToolbarWidgetRegistry],
  activate: async (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    _settingRegistry: ISettingRegistry,
    toolbarRegistry: IToolbarWidgetRegistry
  ) => {
    console.log(
      'JupyterLab extension @e2xgrader/author-assignment-extension is activated!'
    );

    const { commands } = app;
    registerCommands(commands, notebookTracker);

    if (toolbarRegistry) {
      AuthoringMenubar.registerAuthoringToolbarFactory(
        commands,
        toolbarRegistry
      );
    }

    notebookTracker.widgetAdded.connect((_, notebookPanel) => {
      notebookPanel.toolbar.insertItem(
        2,
        'toggleToolbar',
        AuthoringCellToolbar.createToggleAuthoringToolbarButton()
      );
    });
  }
};

export default [plugin, cellFactoryExtension];
