define([
    'jquery',
    'base/js/namespace',
    './extended_cell'
], function (
    $,
    Jupyter,
    extended_cell
) {

    'use strict';

    let ExtendedCell = extended_cell.ExtendedCell;

    class ChoiceCell extends ExtendedCell {

        constructor(cell, type) {
            super(cell, type);
            this.choice_field = 'choice';
            this.edit_mode = false;
        }

        get_choices = function () {
            let metadata = this.get_metadata();
            if (metadata.hasOwnProperty(this.choice_field)) {
                return metadata[this.choice_field];
            }
            return [];
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


    class SinglechoiceCell extends ChoiceCell {

        constructor(cell) {
            super(cell, 'singlechoice');
        }

        set_choice = function (value) {
            let metadata = this.get_metadata();
            metadata[this.choice_field] = [value];
        }

        create_radio_button = function (name, value, selected, onChange) {
            let input = $('<input>')
                                .attr('type', 'radio')
                                .attr('name', name)
                                .attr('value', value)
                                .change(onChange);
            if (selected) {
                input.attr('checked', 'checked');
            }
            return input;
        }

        render = function () {
            this.cell.render_force();
            let html = $(this.cell.element).find('.rendered_html');
            let lists = html.find('ul');
            let choices = this.get_choices();
            let that = this;
            if (lists.length > 0) {
                let list = lists[0];
                let form = $('<form>').addClass('hbrs_radio');
                let items = $(list).find('li');
                if (choices.length > 0 && choices[0] >= items.length) {
                    let metadata = this.get_metadata();
                    metadata[this.choice_field] = [];
                    choices = this.get_choices();
                }
                for (let i=0; i<items.length; i++) {
                    let input = this.create_radio_button('my_radio', i, choices.indexOf(i.toString()) >= 0, function () {
                        that.set_choice(this.value);
                    });
                    Jupyter.keyboard_manager.register_events(input);
                    form.append($('<div>')
                            .append(input)
                            .append('&nbsp;&nbsp;')
                            .append(items[i].childNodes));
                }
                $(list).replaceWith(form);
            }
            if (this.edit_mode) {
                html.append(this.get_edit_button());        
            }
        }

    }


    class MultiplechoiceCell extends ChoiceCell {

        constructor(cell) {
            super(cell, 'multiplechoice');
            this.choice_count_field = 'num_of_choices';
        }

        get_number_of_choices = function () {
            let metadata = this.get_metadata();
            if (metadata.hasOwnProperty(this.choice_count_field)) {
                return metadata[this.choice_count_field];
            }
            return [];
        }

        set_number_of_choices = function (value) {
            let metadata = this.get_metadata();
            metadata[this.choice_count_field] = value;
        }

        add_choice = function (value) {
            let metadata = this.get_metadata();
            let choices = this.get_choices();
            let idx = choices.indexOf(value);
            if (idx > -1) {
                return;
            }
            choices.push(value);
            metadata[this.choice_field] = choices;
        }

        remove_choice = function (value) {
            let metadata = this.get_metadata();
            let choices = this.get_choices();
            let idx = choices.indexOf(value);
            if (idx > -1) {
                choices.splice(idx, 1);
            }
            metadata[this.choice_field] = choices;
        }

        create_checkbox = function (name, value, selected, points) {
            let that = this;
            let input = $('<input>')
                .attr('type', 'checkbox')
                .attr('name', name)
                .attr('value', value)
                .change(function () {
                    if (this.checked) {
                        that.add_choice(this.value);
                    } else {
                        that.remove_choice(this.value);
                    }
                });
            if (selected) {
                input.attr('checked', 'checked');
            }
            return input;
        }

        render = function () {
            this.cell.render_force();
            let html = $(this.cell.element).find('.rendered_html');
            let lists = html.find('ul');
            let that = this;

            if (lists.length > 0) {
                let list = lists[0];
                let form = $('<form>').addClass('hbrs_checkbox');
                let items = $(list).find('li');
                let num_of_choices = this.get_number_of_choices();
                if (num_of_choices != items.length) {
                    this.set_number_of_choices(items.length);
                    let metadata = this.get_metadata();
                    metadata[this.choice_field] = [];
                }
                let choices = this.get_choices();
                for (let i=0; i<items.length; i++) {
                    let input = this.create_checkbox('my_checkbox', i, choices.indexOf(i.toString()) >= 0);
                    Jupyter.keyboard_manager.register_events(input);

                    let input_div = $('<div>')
                        .append(input)
                        .append('&nbsp;&nbsp;')
                        .append(items[i].childNodes);

                    form.append(input_div);
                };
                $(list).replaceWith(form);
            }
            if (this.edit_mode) {
                html.append(this.get_edit_button());        
            }
        }

    }

    return {
        SinglechoiceCell: SinglechoiceCell,
        MultiplechoiceCell: MultiplechoiceCell
    };

});