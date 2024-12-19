import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { HelpAPI } from './api';
import { Menu } from '@lumino/widgets';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

export const PLUGIN_ID = '@e2xgrader/help-extension:plugin';
export const commandIDs = {
  openHelp: 'e2xgrader:open-help'
};

function loadSetting(setting: ISettingRegistry.ISettings, menu: Menu): void {
  menu.title.label = setting.get('menuLabel').composite as string;
}

/**
 * Initialization data for the @e2xgrader/labextension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description:
    'A JupyterLab extension which provides additional resources for e2xgrader',
  autoStart: true,
  requires: [IMainMenu, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    mainMenu: IMainMenu,
    settingRegistry: ISettingRegistry
  ) => {
    console.log('JupyterLab extension @e2xgrader/help-extension is activated!');

    app.commands.addCommand(commandIDs.openHelp, {
      label: (args: any) => args['label'] || 'Open e2xgrader help',
      execute: args => {
        console.log('Opening e2xgrader help', args);
        if (args['url']) {
          const url = args['url'];
          if (typeof url === 'string') {
            window.open(url, '_blank');
          }
        }
      }
    });

    const menu = new Menu({ commands: app.commands });
    menu.title.label = 'E2xgrader';
    settingRegistry.load(PLUGIN_ID).then(setting => {
      loadSetting(setting, menu);
      setting.changed.connect(loadSetting.bind(null, setting, menu));
    });
    menu.id = 'e2xgrader-menu';
    HelpAPI.getHelp().then(help => {
      help.forEach((helpItem: any) => {
        menu.addItem({
          args: { url: HelpAPI.static_url + helpItem[1], label: helpItem[0] },
          command: commandIDs.openHelp
        });
      });
    });
    mainMenu.addMenu(menu);
  }
};

export default [plugin];
