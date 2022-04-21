define([
    'jquery',
    './extended_cell',
    './attachment_view',
    './attachment'
], function (
    $,
    extended_cell,
    attachment_view,
    attachment_model
) {

    'use strict';

    let ExtendedCell = extended_cell.ExtendedCell;

    class AttachmentCell extends ExtendedCell {

        constructor(cell) {            
            super(cell, 'attachments');
            this.model = new attachment_model.AttachmentCellModel(cell);
            this.view = new attachment_view.AttachmentGallery(cell, this.model);
            this.edit_mode = false;
        }

        get_attachment_button() {
            let that = this;
            return $('<button>')
                .attr('type', 'button')
                .addClass('edit_attachments')
                .click(function () {
                    that.view.open();
                }).append('Add Files / Images');
        }

        get_edit_button = function () {
            let that = this;
            return $('<button>')
                .attr('type', 'button')
                .addClass('hbrs_unrender')
                .click(function () {
                    that.cell.unrender_force();
                }).append('Edit cell');
        }

        render = function() {
            this.cell.render_force();
            let html = $(this.cell.element).find('.rendered_html');
            if (html.find('.edit_attachments').length < 1) {
                html.append(this.get_attachment_button());
            }
            if (this.edit_mode) {
                html.append(this.get_edit_button());
            }
        }

    }

    return {
        AttachmentCell: AttachmentCell,
    };

});
