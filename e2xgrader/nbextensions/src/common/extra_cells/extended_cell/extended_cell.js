define([
    'base/js/namespace'
], function (
    Jupyter
) {
    'use strict';

    class ExtendedCell {

        constructor(cell, type) {
            this.field = 'extended_cell';
            this.type = type;
            this.cell = cell;
            if (!this.cell.metadata.hasOwnProperty(this.field)) {
                this.cell.metadata[this.field] = {};
            }
            this.cell.metadata[this.field]['type'] = type;
            this.edit_mode = false;
        }

        get_metadata() {
            if (this.cell.metadata.hasOwnProperty(this.field)) {
                return this.cell.metadata[this.field];
            }
            return {};
        }

        get_edit_button() {
            let that = this;
            let edit_div = $('<div/>');
            edit_div.append($('<hr/>'));
            edit_div.append($('<button/>')
                .attr('type', 'button')
                .addClass('e2x_unrender')
                .click(function () {
                    that.cell.unrender_force();
                }).append('Edit cell'));
            return edit_div;
        }

        add_edit_button() {
            if (!this.edit_mode) {
                return;
            }
            let html = $(this.cell.element).find('.rendered_html');
            if (html.find('.e2x_unrender').length < 1) {
                html.append(this.get_edit_button());
            }
        }

        render() {
            this.cell.render();
        }

    }

    return {
        ExtendedCell: ExtendedCell
    };

});
