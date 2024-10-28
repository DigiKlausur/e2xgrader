import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICellRegistry } from '@e2xgrader/cell-core';
import { CellRegistry } from './registry';

const PLUGIN_ID = '@e2xgrader/cell-registry:plugin';

const plugin: JupyterFrontEndPlugin<ICellRegistry> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension for registering custom e2xgrader cells',
  autoStart: true,
  provides: ICellRegistry,
  activate: (app: JupyterFrontEnd): ICellRegistry => {
    console.log('JupyterLab extension @e2xgrader/cell-registry is activated!');
    const registry = new CellRegistry();
    return registry;
  }
};

export default plugin;
