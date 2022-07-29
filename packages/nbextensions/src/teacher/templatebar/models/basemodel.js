define([], function () {
  "use strict";

  var field = "nbassignment";

  var get_role = function (cell) {
    if (
      cell.metadata.hasOwnProperty(field) &&
      cell.metadata[field].hasOwnProperty("type")
    ) {
      return cell.metadata[field].type;
    }
    return "";
  };

  var set_role = function (cell, role) {
    cell.metadata[field] = {
      type: role,
    };
  };

  var is_header = function (cell) {
    return get_role(cell) === "header";
  };

  var to_header = function (cell) {
    set_role(cell, "header");
  };

  var is_footer = function (cell) {
    return get_role(cell) === "footer";
  };

  var to_footer = function (cell) {
    set_role(cell, "footer");
  };

  var is_student_info = function (cell) {
    return get_role(cell) === "student_info";
  };

  var to_student_info = function (cell) {
    set_role(cell, "student_info");
  };

  var is_group_info = function (cell) {
    return get_role(cell) === "group_info";
  };

  var to_group_info = function (cell) {
    set_role(cell, "group_info");
  };

  var remove_metadata = function (cell) {
    if (cell.metadata.hasOwnProperty(field)) {
      delete cell.metadata[field];
      if (cell.rendered) {
        cell.unrender();
        cell.render();
      }
    }
  };

  return {
    remove_metadata: remove_metadata,
    is_header: is_header,
    to_header: to_header,
    is_footer: is_footer,
    to_footer: to_footer,
    get_role: get_role,
    is_student_info: is_student_info,
    to_student_info: to_student_info,
    is_group_info: is_group_info,
    to_group_info: to_group_info,
  };
});
