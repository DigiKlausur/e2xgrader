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

    var ChoiceCell = function (cell, type) {
        extended_cell.ExtendedCell.call(this, cell, type);
        this.choice_field = 'choice';
        this.edit_mode = false;
    };

    ChoiceCell.prototype = Object.create(extended_cell.ExtendedCell.prototype);

    ChoiceCell.prototype.get_choices = function () {
        var metadata = this.get_metadata();
        if (metadata.hasOwnProperty(this.choice_field)) {
            return metadata[this.choice_field];
        }
        return [];
    };

    ChoiceCell.prototype.get_edit_button = function () {
        var that = this;
        return $('<button>')
            .attr('type', 'button')
            .addClass('hbrs_unrender')
            .click(function () {
                that.cell.unrender_force();
            }).append('Edit cell');
    };

    var SinglechoiceCell = function (cell) {
        ChoiceCell.call(this, cell, 'singlechoice');
    }

    SinglechoiceCell.prototype = Object.create(ChoiceCell.prototype);

    SinglechoiceCell.prototype.set_choice = function (value) {
        var metadata = this.get_metadata();
        metadata[this.choice_field] = [value];
    };

    SinglechoiceCell.prototype.create_radio_button = function (name, value, selected, onChange) {
        var input = $('<input>')
                            .attr('type', 'radio')
                            .attr('name', name)
                            .attr('value', value)
                            .change(onChange);
        if (selected) {
            input.attr('checked', 'checked');
        }
        return input;
    };

    SinglechoiceCell.prototype.render = function () {
        this.cell.render_force();
        var html = $(this.cell.element).find('.rendered_html');
        var lists = html.find('ul');
        var choices = this.get_choices();
        var that = this;
        if (lists.length > 0) {
            var list = lists[0];
            var form = $('<form>').addClass('hbrs_radio');
            var items = $(list).find('li');
            if (choices.length > 0 && choices[0] >= items.length) {
                var metadata = this.get_metadata();
                metadata[this.choice_field] = [];
                choices = this.get_choices();
            }
            for (var i=0; i<items.length; i++) {
                var input = this.create_radio_button('my_radio', i, choices.indexOf(i.toString()) >= 0, function () {
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
    };

    var MultiplechoiceCell = function (cell) {
        ChoiceCell.call(this, cell, 'multiplechoice');
        this.weight_field = 'weights';
        this.choice_count_field = 'num_of_choices';
    };

    MultiplechoiceCell.prototype = Object.create(ChoiceCell.prototype);

    MultiplechoiceCell.prototype.get_number_of_choices = function () {
        var metadata = this.get_metadata();
        if (metadata.hasOwnProperty(this.choice_count_field)) {
            return metadata[this.choice_count_field];
        }
        return [];
    }

    MultiplechoiceCell.prototype.set_number_of_choices = function (value) {
        var metadata = this.get_metadata();
        metadata[this.choice_count_field] = value;
    }

    MultiplechoiceCell.prototype.add_choice = function (value) {
        var metadata = this.get_metadata();
        var choices = this.get_choices();
        var idx = choices.indexOf(value);
        if (idx > -1) {
            return;
        }
        choices.push(value);
        metadata[this.choice_field] = choices;
    };

    MultiplechoiceCell.prototype.remove_choice = function (value) {
        var metadata = this.get_metadata();
        var choices = this.get_choices();
        var idx = choices.indexOf(value);
        if (idx > -1) {
            choices.splice(idx, 1);
        }
        metadata[this.choice_field] = choices;
    };

    MultiplechoiceCell.prototype.create_checkbox = function (name, value, selected, points) {
        var that = this;
        var input = $('<input>')
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
    };

    MultiplechoiceCell.prototype.render = function () {
        this.cell.render_force();
        var html = $(this.cell.element).find('.rendered_html');
        var lists = html.find('ul');
        var that = this;

        if (lists.length > 0) {
            var list = lists[0];
            var form = $('<form>').addClass('hbrs_checkbox');
            var items = $(list).find('li');
            var num_of_choices = this.get_number_of_choices();
            if (num_of_choices != items.length) {
                this.set_number_of_choices(items.length);
                var metadata = this.get_metadata();
                metadata[this.choice_field] = [];
            }
            var choices = this.get_choices();
            for (var i=0; i<items.length; i++) {
                var input = this.create_checkbox('my_checkbox', i, choices.indexOf(i.toString()) >= 0);
                Jupyter.keyboard_manager.register_events(input);

                var input_div = $('<div>')
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

    return {
        SinglechoiceCell: SinglechoiceCell,
        MultiplechoiceCell: MultiplechoiceCell
    };

});
