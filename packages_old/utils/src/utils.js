const nbgrader_metadata_field = "nbgrader";
export const nbgrader_schema_version = 3;

/**
 * Generate a random string
 * @param  {int} length of the string
 * @return {string} random string
 */
export function randomString(length) {
  let result = "";
  let chars = "abcdef0123456789";
  let i;
  for (i = 0; i < length; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
}

/**
 * Convert value to float
 * @param  {string} value
 * @return {float} value as float
 */
export function to_float(value) {
  if (value === undefined || value === "") {
    return 0;
  }
  return parseFloat(value);
}

/**
 * Does this cell have nbgrader metadata?
 * @param  {Cell}
 * @return {Boolean} - has nbgrader metadata
 */
export function is_nbgrader(cell) {
  return cell.metadata.hasOwnProperty(nbgrader_metadata_field);
}

/**
 * Remove the nbgrader metadata from the cell
 * @param {Cell} cell
 */
export function remove_nbgrader_metadata(cell) {
  if (is_nbgrader(cell)) {
    delete cell.metadata[nbgrader_metadata_field];
    if (cell.rendered) {
      cell.unrender();
      cell.render();
    }
  }
}

/**
 * Create an empty nbgrader metadata object
 * @param {Cell} cell
 * @param {string} type
 */
export function create_nbgrader_metadata(cell) {
  if (!is_nbgrader(cell)) {
    cell.metadata[nbgrader_metadata_field] = {};
  }
}

/**
 * Get the value of an entry in the nbgrader metadata
 * Return the default value if it does not exist
 * @param {Cell} cell
 * @param {string} field
 * @param {any} default_value
 * @returns
 */
export function get_nbgrader_field(cell, field, default_value = {}) {
  if (is_nbgrader(cell)) {
    return cell.metadata[nbgrader_metadata_field][field] || default_value;
  }
  return default_value;
}

/**
 * Set the value of an entry in the nbgrader metadata
 * @param {Cell} cell
 * @param {string} key
 * @param {any} value
 */
export function set_nbgrader_field(cell, key, value) {
  if (!is_nbgrader(cell)) {
    cell.metadata[nbgrader_metadata_field] = {};
  }
  cell.metadata[nbgrader_metadata_field][key] = value;
}

/**
 * Remove a key from the nbgrader metadata *
 * @param {Cell}
 * @param {string} key
 */
export function remove_nbgrader_field(cell, key) {
  if (
    is_nbgrader(cell) &&
    cell.metadata[nbgrader_metadata_field].hasOwnProperty(key)
  ) {
    delete cell.metadata[nbgrader_metadata_field][key];
  }
}

/**
 * Get the nbgrader schema version
 * @param  {Cell} cell
 * @return {int}  nbgrader schema version
 */
export function get_schema_version(cell) {
  if (!is_nbgrader(cell)) {
    return undefined;
  }
  if (get_nbgrader_field(cell, "schema_version") === undefined) {
    return 0;
  }
  return get_nbgrader_field(cell, "schema_version");
}

/**
 * Set the nbgrader schema to the current version
 * @param  {Cell} cell
 */
export function set_schema_version(cell) {
  if (!is_nbgrader(cell)) {
    create_nbgrader_metadata(cell);
  }
  set_nbgrader_field(cell, "schema_version", nbgrader_schema_version);
}

/**
 * Is the cell a solution cell?
 * @param  {Cell} cell
 * @return {Boolean} is solution?
 */
export function is_solution(cell) {
  return get_nbgrader_field(cell, "solution", false);
}

/**
 * Set value for the solution field
 * @param  {Cell}
 * @param  {Boolean} value - the value of the solution field
 */
export function set_solution(cell, value) {
  set_nbgrader_field(cell, "solution", value);
}

/**
 * Is the cell a grade cell?
 * @param  {Cell} cell
 * @return {Boolean} is grade?
 */
export function is_grade(cell) {
  return get_nbgrader_field(cell, "grade", false);
}

/**
 * Set value for the grade field
 * @param  {Cell} cell
 * @param  {Boolean} value - the value of the grade field
 */
export function set_grade(cell, value) {
  set_nbgrader_field(cell, "grade", value);
}

/**
 * Is the cell a task cell?
 * @param  {Cell} cell
 * @return {Boolean} - is task?
 */
export function is_task(cell) {
  return get_nbgrader_field(cell, "task", false);
}

/**
 * Set value for the task field
 *
 * @param  {Cell}
 * @param  {Boolean} value - the value of the task field
 */
export function set_task(cell, value) {
  set_nbgrader_field(cell, "task", value);
}

/**
 * Is the cell locked?
 * @param  {Cell} cell
 * @return {Boolean} - is locked?
 */
export function is_locked(cell) {
  return get_nbgrader_field(cell, "locked", false);
}

/**
 * Set value for the locked field
 * @param  {Cell} cell
 * @param  {Boolean} value - the value of the locked field
 */
export function set_locked(cell, value) {
  set_nbgrader_field(cell, "locked", value);
}

/**
 * Get the number of points for this cell
 * @param  {Cell} cell
 * @return {float} - points
 */
export function get_points(cell) {
  return to_float(get_nbgrader_field(cell, "points", 0));
}

/**
 * Set the number of points for this cell
 * @param  {Cell} cell
 * @param  {float} points
 */
export function set_points(cell, points) {
  set_nbgrader_field(cell, "points", Math.max(0, to_float(points)));
}

/**
 * Get the grade id for this cell
 * @param  {Cell} cell
 * @return {string} - grade id
 */
export function get_grade_id(cell) {
  return get_nbgrader_field(cell, "grade_id", "cell-" + randomString(16));
}

/**
 * Set the grade id for this cell
 * @param  {Cell} cell
 * @param  {string} grade_id
 */
export function set_grade_id(cell, grade_id) {
  set_nbgrader_field(cell, "grade_id", grade_id);
}

/**
 * Is this cell a test cell?
 * @param  {Cell}
 * @return {Boolean}
 */
export function is_test(cell) {
  return is_grade(cell) && is_locked(cell) && !is_solution(cell);
}

/**
 * Turn this cell into a test cell
 * @param  {Cell}
 */
export function to_test(cell) {
  remove_metadata(cell);
  set_schema_version(cell);
  set_solution(cell, false);
  set_grade(cell, true);
  set_locked(cell, true);
}

/**
 * Is this cell a description cell?
 * @param  {Cell}
 * @return {Boolean}
 */
export function is_description(cell) {
  return is_locked(cell) && !is_grade(cell) && !is_solution(cell);
}

/**
 * Turn this cell into a description cell
 * @param  {Cell}
 */
export function to_description(cell) {
  remove_metadata(cell);
  set_schema_version(cell);
  set_solution(cell, false);
  set_grade(cell, false);
  set_locked(cell, true);
}

export function is_invalid(cell) {
  if (is_task(cell)) {
    return false;
  } else if (is_solution(cell) && is_grade(cell)) {
    return false;
  } else if (is_solution(cell) && cell.cell_type !== "code") {
    return true;
  } else if (is_grade(cell) && cell.cell_type !== "code") {
    return true;
  }
  return false;
}

export function is_empty(cell) {
  return cell.get_text().length == 0;
}
