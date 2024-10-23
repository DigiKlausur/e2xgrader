import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { hello_world } from '@e2xgrader/cells';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

/**
 * Initialization data for the @e2xgrader/labextension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@e2xgrader/labextension:plugin',
  description: 'A JupyterLab extension which bundles e2xgrader extensions',
  autoStart: true,
  optional: [ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    settingRegistry: ISettingRegistry | null
  ) => {
    console.log('JupyterLab extension @e2xgrader/labextension is activated!');
    hello_world();
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log(
            '@e2xgrader/labextension settings loaded:',
            settings.composite
          );
        })
        .catch(reason => {
          console.error(
            'Failed to load settings for @e2xgrader/labextension.',
            reason
          );
        });
    }
  }
};

export default [plugin];
