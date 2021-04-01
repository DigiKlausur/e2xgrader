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

    let is_attachment = function (cell) {
        return cell_type(cell) === 'attachments';
    };

    let to_attachment = function (cell) {
        cell.metadata[field] = {
            'type': 'attachments'
        };
    };

    let is_pdf = function (cell) {
        return cell_type(cell) === 'pdf';
    };

    let to_pdf = function (cell) {
        cell.metadata[field] = {
            'type': 'pdf'
        };
    };

    let is_form = function (cell) {
        return cell_type(cell) === 'form';
    };

    let to_form = function (cell) {
        cell.metadata[field] = {
            'type': 'form'
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
        to_multiplechoice: to_multiplechoice,
        is_attachment: is_attachment,
        to_attachment: to_attachment,
        is_pdf: is_pdf,
        to_pdf: to_pdf,
        is_form: is_form,
        to_form: to_form,
    };
})