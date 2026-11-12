import utils from "base/js/utils";

// Notebook 7 serves /tree and /notebooks; the classic UI lives under /nbclassic
const CLASSIC_PREFIX = "nbclassic";

/**
 * Build a link to a directory or file in the classic notebook file browser.
 *
 * @param {string} base_url - The server's base URL.
 * @param {string} path - Path relative to the server root; gets URL-encoded.
 * @returns {string} <base_url>/nbclassic/tree/<path>
 */
export function tree_url(base_url, path) {
  return utils.url_path_join(
    base_url,
    CLASSIC_PREFIX,
    "tree",
    utils.url_join_encode(path)
  );
}

/**
 * Build a link that opens a notebook in the classic notebook UI.
 *
 * @param {string} base_url - The server's base URL.
 * @param {string} path - Notebook path relative to the server root; gets URL-encoded.
 * @returns {string} <base_url>/nbclassic/notebooks/<path>
 */
export function notebook_url(base_url, path) {
  return utils.url_path_join(
    base_url,
    CLASSIC_PREFIX,
    "notebooks",
    utils.url_join_encode(path)
  );
}
