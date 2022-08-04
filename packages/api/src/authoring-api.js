import { BaseAPI } from "./base";
import { pathJoin } from "./base";

export class AuthoringAPI extends BaseAPI {
  constructor(base_url) {
    super();
    this.base_url = pathJoin([base_url, "taskcreator", "api"]);
  }

  get_presets(params) {
    return this.get(pathJoin([this.base_url, "presets"]), params);
  }

  list_question_presets() {
    return this.get_presets({
      type: "question",
      action: "list",
    });
  }

  list_template_presets() {
    return this.get_presets({
      type: "template",
      action: "list",
    });
  }

  get_question_preset(name) {
    return this.get_presets({
      type: "question",
      action: "get",
      name: name,
    });
  }

  get_template_preset(name) {
    return this.get_presets({
      type: "template",
      action: "get",
      name: name,
    });
  }
}
