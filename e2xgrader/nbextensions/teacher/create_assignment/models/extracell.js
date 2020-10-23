define([
], function () {

    'use strict';

    let field = 'extended_cell';

    let cell_type = function (cell) {
        if (cell.metadata.hasOwnProperty(field)) {
            return cell.metadata.extended_cell.type;
        }
        return cell.cell_type;
    };

    let is_extracell = function (cell) {
        return cell.metadata.hasOwnProperty(field);
    };

    let is_multiplechoice = function (cell) {
        return cell_type(cell) === 'multiplechoice';
    };

    let to_multiplechoice = function (cell) {
        cell.metadata[field] = {
            'type': 'multiplechoice'
        };
    };

    let is_singlechoice = function (cell) {
        return cell_type(cell) === 'singlechoice';
    };

    let to_singlechoice = function (cell) {
        cell.metadata[field] = {
            'type': 'singlechoice'
        };
    };

    let remove_metadata = function (cell) {
        if (cell.metadata.hasOwnProperty(field)) {
            delete cell.metadata.extended_cell;
            if (cell.rendered) {
                cell.unrender();
                cell.render();
            }
        }
    };

    return {
        remove_metadata: remove_metadata,
        is_singlechoice: is_singlechoice,
        to_singlechoice: to_singlechoice,
        is_multiplechoice: is_multiplechoice,
        to_multiplechoice: to_multiplechoice
    };
})