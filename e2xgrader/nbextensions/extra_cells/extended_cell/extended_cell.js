define([
    'base/js/namespace'
], function (
    Jupyter
) {
    'use strict';

    var ExtendedCell = function (cell, type) {
        this.field = 'extended_cell';
        this.type = type;
        this.cell = cell;
        if (!this.cell.metadata.hasOwnProperty(this.field)) {
            this.cell.metadata[this.field] = {};
        }
        this.cell.metadata[this.field]['type'] = type;
    };

    ExtendedCell.prototype.get_metadata = function () {
        if (this.cell.metadata.hasOwnProperty(this.field)) {
            return this.cell.metadata[this.field];
        }
        return {};
    };

    ExtendedCell.prototype.render = function () {
        this.cell.render();
    };

    return {
        ExtendedCell: ExtendedCell
    };

});