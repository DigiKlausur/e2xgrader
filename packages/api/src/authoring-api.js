import { BaseAPI, pathJoin } from "./base";

export class AuthoringAPI extends BaseAPI {
  constructor(base_url) {
    super();
    this.base_url = pathJoin([base_url, "e2x", "authoring", "api"]);
  }

  get_presets(params) {
    return this.get(pathJoin([this.base_url, "presets"]), params);
  }

  list_question_presets() {
    return this.get_presets({
      action: "list_question_presets",
    });
  }

  list_template_presets() {
    return this.get_presets({
      action: "list_template_presets",
    });
  }

  get_question_preset(name) {
    return this.get_presets({
      action: "get_question_preset",
      preset_name: name,
    });
  }

  get_template_preset(name) {
    return this.get_presets({
      action: "get_template_preset",
      preset_name: name,
    });
  }
}
