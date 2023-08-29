import Jupyter from "base/js/namespace";
import { requests, urlJoin } from "@e2xgrader/api";

const PRESET_API_ROOT = urlJoin(
  Jupyter.notebook.base_url,
  "e2x",
  "authoring",
  "api",
  "presets"
);

const API = {
  list_question_presets: () =>
    requests.get(PRESET_API_ROOT, { action: "list_question_presets" }),
  list_template_presets: () =>
    requests.get(PRESET_API_ROOT, { action: "list_template_presets" }),
  get_question_preset: (name) =>
    requests.get(PRESET_API_ROOT, {
      action: "get_question_preset",
      preset_name: name,
    }),
  get_template_preset: (name) =>
    requests.get(PRESET_API_ROOT, {
      action: "get_template_preset",
      preset_name: name,
    }),
};

export default API;
