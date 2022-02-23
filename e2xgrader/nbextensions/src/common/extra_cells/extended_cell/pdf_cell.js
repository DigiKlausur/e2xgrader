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
        }

        render() {
            this.cell.unsafe_render();
            this.add_edit_button();
        }

    }

    return {
        PDFCell: PDFCell,
    };

});
