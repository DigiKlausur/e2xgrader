define([
    'jquery',
    'base/js/namespace',
    './extended_cell',
], function (
    $,
    Jupyter,
    extended_cell,
) {

    'use strict';

    let ExtendedCell = extended_cell.ExtendedCell;

    class FormCell extends ExtendedCell {

        constructor(cell) {
            super(cell, 'form');
            this.data_field = 'choices';
        }

        get_choices() {
            let metadata = this.get_metadata();
            if (metadata.hasOwnProperty(this.data_field)) {
                return metadata[this.data_field];
            }
            return {};
        }

        set_choices(choices) {
            let metadata = this.get_metadata();
            metadata[this.data_field] = choices;
        }

        set_choice(field, value) {
            let metadata = this.get_metadata();
            metadata[this.data_field][field]['value'] = value;
        }

        get_choice(field) {
            return this.get_metadata()[this.data_field][field]['value'];
        }

        find_form_elements() {
            let elements = {};
            let html = $(this.cell.element).find('.rendered_html');
            for (let input of html.find('input')) {
                let name = $(input).attr('name');
                if (name === undefined) {
                    // TODO: Maybe raise validation error
                    continue;
                }
                if (elements.hasOwnProperty(name)) {
                    elements[name]['nodes'].push(input);
                } else {
                    let type = $(input).attr('type');
                    elements[name] = {
                        'type': type === undefined ? 'text' : type,
                        'nodes': [input]
                    };
                }
            }

            for (let select of html.find('select')) {
                let name = $(select).attr('name');
                if (name === undefined) {
                    // TODO: Maybe raise validation error
                    continue;
                }
                elements[name] = {
                    'type': 'select',
                    'nodes': select
                };
            }

            return elements;
        }

        connect_form_elements(elements) {
            let that = this;
            for (let name of Object.keys(elements)) {
                let type = elements[name]['type'];
                if (type === 'radio') {
                    for (let node of elements[name]['nodes']) {
                        $(node).change(function () {
                            that.set_choice(name, this.value);
                        })
                        Jupyter.keyboard_manager.register_events($(node));
                    }
                } else if (type === 'checkbox') {
                    for (let node of elements[name]['nodes']) {
                        $(node).change(function () {
                            let value = that.get_choice(name);
                            if (this.checked) {
                                value.push(this.value);
                            } else {
                                let idx = value.indexOf(this.value);
                                if (idx > -1) {
                                    value.splice(idx, 1);
                                }
                            }
                            that.set_choice(name, value);
                        })
                        Jupyter.keyboard_manager.register_events($(node));
                    }
                } else {
                    $(elements[name]['nodes']).change(function () {
                        that.set_choice(name, this.value);
                    })
                    Jupyter.keyboard_manager.register_events($(elements[name]['nodes']));
                }
            }
        }

        sanitize_choices(elements) {
            let data = this.get_choices();
            for (let name of Object.keys(data)) {
                let type = data[name]['type'];
                if (!elements.hasOwnProperty(name) || type !== elements[name]['type']) {
                    // If there is no element with the name or the type has changed, delete the entry
                    delete data[name]
                } else {
                    let value = data[name]['value'];
                    // Make sure the value in data exists as an element
                    if (type === 'radio') {
                        let valid_values = [];
                        for (let node of elements[name]['nodes']) {
                            valid_values.push($(node).attr('value'));
                        }
                        if (!valid_values.includes(value)) {
                            value = undefined;
                        }
                    } else if (type === 'checkbox') {
                        let valid_values = [];
                        for (let node of elements[name]['nodes']) {
                            valid_values.push($(node).attr('value'));
                        }
                        value = value.filter(val => valid_values.includes(val));
                    } else if (type === 'select' && $(elements[name]['nodes']).find('option[value="' + value + '"]').length < 1) {
                        value = $(elements[name]['nodes']).find('option').val();
                    }
                    data[name]['value'] = value;
                }
            }
            this.set_choices(data);
        }


        render() {
            this.cell.unsafe_render();
            let html = $(this.cell.element).find('.rendered_html');

            let elements = this.find_form_elements();

            this.sanitize_choices(elements);
            let data = this.get_choices();

            // Update the data field
            for (let name of Object.keys(elements)) {
                let type = elements[name]['type'];
                if (!data.hasOwnProperty(name)) {
                    // Read value of element and store in data
                    let value;

                    if (type === 'radio') {
                        value = html.find('input[name="' + name + '"]:checked').val();
                    } else if (type === 'checkbox') {
                        value = [];
                        for (let input of html.find('input[name="' + name + '"]:checked')) {
                            value.push($(input).val());
                        }
                    } else {
                        value = $(elements[name]['nodes'][0]).val();
                    }
                    data[name] = {
                        'type': elements[name]['type'],
                        'value': value
                    }
                } else {
                    // Read value from data and set elements
                    let value = data[name]['value'];
                    if (value !== undefined) {
                        if (type === 'radio') {
                            for (let node of elements[name]['nodes']) {
                                if ($(node).val() === value) {
                                    $(node).attr('checked', 'checked');
                                }
                            }
                        } else if (type === 'checkbox') {
                            for (let node of elements[name]['nodes']) {
                                if (value.includes($(node).val())) {
                                    $(node).attr('checked', 'checked');
                                }
                            }
                        } else if (type === 'select') {
                            for (let option of $(elements[name]['nodes']).find('option')) {
                                if (value == $(option).attr('value')) {
                                    $(option).attr('selected', 'selected');
                                } else {
                                    $(option).removeAttr('selected');
                                }
                            }
                        } else {
                            $(elements[name]['nodes']).val(value);
                        }
                    }
                }
            }

            // Save data
            this.set_choices(data);

            // Connect data to elements with callbacks
            this.connect_form_elements(elements);

            this.add_edit_button();
        }

    }

    return {
        FormCell: FormCell,
    };

});
