import { ISettingRegistry } from '@jupyterlab/settingregistry';

export class Settings {
  private static instances: Map<string, ISettingRegistry.ISettings> = new Map();
  private static initializationPromises: Map<string, Promise<void>> = new Map();

  private constructor() {}

  /**
   * Retrieves the settings instance for the specified plugin ID.
   *
   * This method ensures that the settings instance is initialized before returning it.
   * If the settings instance is not initialized, it throws an error.
   *
   * @param pluginId - The unique identifier of the plugin whose settings are to be retrieved.
   * @returns A promise that resolves to the settings instance for the specified plugin ID.
   * @throws An error if the settings instance for the specified plugin ID is not initialized.
   */
  public static async getInstance(
    pluginId: string
  ): Promise<ISettingRegistry.ISettings> {
    if (Settings.initializationPromises.has(pluginId)) {
      await Settings.initializationPromises.get(pluginId);
    }
    const instance = Settings.instances.get(pluginId);
    if (!instance) {
      throw new Error(
        `SettingsRegistry for plugin ID ${pluginId} is not initialized`
      );
    }
    return instance;
  }

  /**
   * Initializes the settings for a given plugin.
   *
   * @param pluginId - The unique identifier for the plugin.
   * @param settings - The settings registry to load the plugin settings from.
   * @returns A promise that resolves when the settings have been successfully loaded.
   * @throws An error if the settings for the given plugin ID are already initialized.
   */
  public static initialize(
    pluginId: string,
    settings: ISettingRegistry
  ): Promise<void> {
    if (Settings.instances.has(pluginId)) {
      throw new Error(
        `SettingsRegistry for plugin ID ${pluginId} is already initialized`
      );
    }
    const initializationPromise = settings.load(pluginId).then(setting => {
      Settings.instances.set(pluginId, setting);
    });
    Settings.initializationPromises.set(pluginId, initializationPromise);
    return initializationPromise;
  }
}

export default Settings;
