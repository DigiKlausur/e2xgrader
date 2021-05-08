define([
    'jquery',
    './extended_cell',
], function (
    $,
    extended_cell,
) {

    'use strict';

    let ExtendedCell = extended_cell.ExtendedCell;

    class PDFCell extends ExtendedCell {

        constructor(cell) {            
            super(cell, 'pdf');
            this.edit_mode = false;
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

    }

    return {
        PDFCell: PDFCell,
    };

});
