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

    }

    return {
        PDFCell: PDFCell,
    };

});
