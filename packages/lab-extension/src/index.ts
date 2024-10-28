import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICellRegistry } from '@e2xgrader/cell-core';

/**
 * Initialization data for the @e2xgrader/labextension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@e2xgrader/labextension:plugin',
  description: 'A JupyterLab extension which bundles e2xgrader extensions',
  autoStart: true,
  requires: [ICellRegistry],
  activate: (app: JupyterFrontEnd, cellRegistry: ICellRegistry) => {
    console.log('JupyterLab extension @e2xgrader/labextension is activated!');

    console.log('Cell registry:', cellRegistry);
    cellRegistry.cellRegistered.connect((_, { type, cellClass }) => {
      console.log('Cell registered:', type, cellClass);
    });
  }
};

export default [plugin];
