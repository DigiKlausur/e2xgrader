import Jupyter from "base/js/namespace";
import dialog from "base/js/dialog";
import { utils } from "@e2xgrader/utils";

export class NbgraderValidator {
  constructor() {
    this.warning = undefined;
    this.grade_id_regex = /^[a-zA-Z0-9_-]+$/;
  }

  /**
   * Get basic modal options
   */
  get_modal_opts() {
    let that = this;
    return {
      notebook: Jupyter.notebook,
      keyboard_manager: Jupyter.keyboard_manager,
      buttons: {
        OK: {
          class: "btn-primary",
          click: function () {
            that.warning = undefined;
          },
        },
      },
    };
  }

  /**
   * Validate the nbgrader grade ids
   * Display a warning if there are invalid or duplicate ids
   */
  validate_ids() {
    if (this.warning !== undefined) {
      return;
    }

    let modal_opts = this.get_modal_opts();
    let elems = $(".nbgrader-id-input");
    let set = new Object();

    for (const element of elems) {
      let label = $(element).val();
      if (!this.grade_id_regex.test(label)) {
        modal_opts.title = "Invalid nbgrader cell ID";
        modal_opts.body =
          "At least one cell has an invalid nbgrader ID. Cell IDs must contain at least one character, and may only contain letters, numbers, hyphens, and/or underscores.";
        this.warning = dialog.modal(modal_opts);
        break;
      } else if (label in set) {
        modal_opts.title = "Duplicate nbgrader cell ID";
        modal_opts.body =
          'The nbgrader ID "' +
          label +
          '" has been used for more than one cell. Please make sure all grade cells have unique ids.';
        this.warning = dialog.modal(modal_opts);
        break;
      } else {
        set[label] = true;
      }
    }
  }

  /**
   * Validate the nbgrader schema version
   * Display a warning if the schema is outdated
   */
  validate_schema_version() {
    if (this.warning !== undefined) {
      return;
    }

    let cells = Jupyter.notebook.get_cells();
    let modal_opts = this.get_modal_opts();

    for (const cell of cells) {
      let schema = utils.get_schema_version(cell);
      if (schema !== undefined && schema < utils.nbgrader_schema_version) {
        modal_opts.title = "Outdated schema version";
        modal_opts.body = $("<p/>").html(
          "At least one cell has an old version (" +
            schema +
            ") of the " +
            "nbgrader metadata. Please back up this notebook and then " +
            "update the metadata on the command " +
            "line using the following command: <code>nbgrader update " +
            Jupyter.notebook.notebook_path +
            "</code>"
        );
        this.warning = dialog.modal(modal_opts);
        break;
      }
    }
  }
}
