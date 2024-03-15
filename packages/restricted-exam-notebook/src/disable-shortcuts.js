import { shortcuts as utils } from "@e2xgrader/utils";

export function disable_shortcuts() {
  const shortcuts = [
    "x",
    "c",
    "v",
    "a",
    "b",
    "shift-v",
    "shift-m",
    "y",
    "m",
    "r",
    "ctrl-shift-f",
    "ctrl-shift-p",
    "p",
    "d,d",
  ];

  const modes = ["command", "edit"];

  for (let mode of modes) {
    utils.remove_shortcuts(mode, ...shortcuts);
  }

  utils.remove_shortcuts("command", "crtl-v");

  utils.disable_add_cell_on_execute();

  utils.add_shortcut(
    "command",
    "ctrl-v",
    function (event) {
      return false;
    },
    "no action"
  );
}
