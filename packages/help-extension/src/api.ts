import { Requests } from '@e2xgrader/api';
import { PageConfig } from '@jupyterlab/coreutils';

export namespace HelpAPI {
  export const url = PageConfig.getBaseUrl() + 'e2x/help/api/files';
  export const static_url = PageConfig.getBaseUrl() + 'e2x/help/static/';
  export const getHelp = async () => {
    const response = await Requests.get(url);
    return response.json();
  };
}
