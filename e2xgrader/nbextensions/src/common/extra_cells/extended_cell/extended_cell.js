define([
    'jquery'
], function(
    $
) {

    'use strict';

    class ExtendedCell {

        constructor(cell, type, options = {}) {
            this.field = 'extended_cell';
            this.type = type;
            this.cell = cell;
            
            if (!this.cell.metadata.hasOwnProperty(this.field)) {
                this.cell.metadata[this.field] = {};
            }
            this.cell.metadata[this.field]['type'] = type;
            this.update_options(options);
            this.edit_mode = false;
        }

        update_options(options) {
            // Remove all keys that are not in the options dict
            // Add all keys that are not in metadata
            if (!this.cell.metadata[this.field].hasOwnProperty('options')) {
                this.cell.metadata[this.field]['options'] = options;
                return
            }

            let old_options = this.cell.metadata[this.field]['options'];
            let updated_options = {};
            for (const [key, value] of Object.entries(options)) {
                if (old_options.hasOwnProperty(key)) {
                    updated_options[key] = old_options[key];
                } else {
                    updated_options[key] = value;
                }
            }
            this.cell.metadata[this.field]['options'] = updated_options;
        }

        get_metadata() {
            if (this.cell.metadata.hasOwnProperty(this.field)) {
                return this.cell.metadata[this.field];
            }
            return {};
        }

        render_grader_settings() {
            if (!this.edit_mode) {
                return;
            }
            let that = this;
            let html = $(this.cell.element).find('.rendered_html');
            // Remove old div
            html.find('.e2x_grader_options').remove();
            let container = $('<div/>').addClass('e2x_grader_options');

            container.append($('<hr/>'));

            container.append(this.get_options());
            container.append($('<button/>')
                .attr('type', 'button')
                .addClass('e2x_unrender')
                .click(function() {
                    that.cell.unrender_force();
                }).append('Edit cell'));
            html.append(container);
        }

        get_options() {
            let that = this;
            let container = $('<div/>').addClass('e2x_options');

            for (const [key, value] of Object.entries(this.cell.metadata[this.field]['options'])) {

                if (value['type'] == 'checkbox') {
                    let node = $('<div/>');
                    let input = $('<input/>').attr('type', value['type']);
                    node.append(input);
                    node.append($('<span/>').text(value['text']));                    

                    if (value['value']) {
                        input.attr('checked', 'checked');
                    }
                    input.change(function() {
                        that.cell.metadata[that.field]['options'][key]['value'] = !!this.checked;
                    });
                    container.append(node);
                }
            }
            return container;
        }

        render() {
            this.cell.render();
        }       

    }

    return {
        ExtendedCell: ExtendedCell
    };

});