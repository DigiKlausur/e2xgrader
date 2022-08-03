const e2x_metadata_field = "extended_cell";

/**
 * Does this cell have e2x metadata?
 * @param {Cell} cell
 * @returns {Boolean} - has e2x metadata
 */
export function is_e2x(cell) {
  return (
    cell.hasOwnProperty("metadata") &&
    cell.metadata.hasOwnProperty(e2x_metadata_field)
  );
}

/**
 * Remove the e2x metadata from the cell
 * @param {Cell} cell
 */
export function remove_e2x_metadata(cell) {
  if (is_e2x(cell)) {
    delete cell.metadata[e2x_metadata_field];
    if (cell.rendered) {
      cell.unrender();
      cell.render();
    }
  }
}

/**
 * Create an empty e2x metadata object with a type
 * @param {Cell} cell
 * @param {string} type
 */
export function create_e2x_metadata(cell, type) {
  if (!is_e2x(cell)) {
    cell.metadata[e2x_metadata_field] = {
      type: type,
    };
  }
}

/**
 * Get the e2x metadata
 * @param {Cell} cell
 * @returns {Object} e2x metadata
 */
export function get_e2x_metadata(cell) {
  if (is_e2x(cell)) {
    return cell.metadata[e2x_metadata_field];
  }
  return {};
}

/**
 * Get the e2x cell type
 * @param  {Cell}
 * @return {string} - e2x cell type
 */
export function get_e2x_cell_type(cell) {
  return get_e2x_field(cell, "type", "");
}

/**
 * Get the value of an entry in the e2x metadata
 * Return the default value if it does not exist
 * @param {Cell} cell
 * @param {string} field
 * @param {any} default_value
 * @returns
 */
export function get_e2x_field(cell, field, default_value = {}) {
  if (is_e2x(cell)) {
    return cell.metadata[e2x_metadata_field][field] || default_value;
  }
  return default_value;
}

/**
 * Set the value of an entry in the e2x metadata
 * @param {Cell} cell
 * @param {string} field
 * @param {any} value
 */
export function set_e2x_field(cell, field, value) {
  if (is_e2x(cell)) {
    cell.metadata[e2x_metadata_field][field] = value;
  }
}
