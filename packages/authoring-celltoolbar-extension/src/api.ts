import { Requests } from '@e2xgrader/api';
import { PageConfig } from '@jupyterlab/coreutils';

export namespace AuthoringAPI {
  export const url = PageConfig.getBaseUrl() + 'e2x/authoring/api';
  export const presetUrl = url + '/presets';
  export const listQuestionPresets = async () => {
    const response = await Requests.get(presetUrl, {
      action: 'list_question_presets'
    });
    return response.json();
  };
  export const getQuestionPreset = async (question_type: string) => {
    const response = await Requests.get(presetUrl, {
      action: 'get_question_preset',
      preset_name: question_type
    });
    return response.json();
  };
}
