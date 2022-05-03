define([], function() {

	class OptionDict {

		constructor(cell, options) {
			this.cell = cell;
			this.options = options;
			this.initialize_options();
		}

		initialize_options() {
			let current_options = this.cell.metadata['extended_cell']['options'] || {};
			// Remove all options that are not in the cell options
			let to_remove = [];
			Object.keys(current_options).forEach(key => {
				if (!this.options.hasOwnProperty(key)) {
					to_remove.push(key);
				}
			});

			to_remove.map((key) => delete current_options[key]);
			this.cell.metadata['extended_cell']['options'] = current_options;
		}

		set_option(key, value) {
			this.cell.metadata['extended_cell']['options'][key] = value;
		}

		get_option(key) {
			if (this.cell.metadata['extended_cell']['options'].hasOwnProperty(key)) {
				return this.cell.metadata['extended_cell']['options'][key];
			}
			return this.options[key]['value'];
		}

		render() {
            let that = this;
            let container = $('<div/>').addClass('e2x_options');

            for (const [key, value] of Object.entries(this.options)) {

                if (value['type'] == 'checkbox') {
                    let node = $('<div/>');
                    let input = $('<input/>').attr('type', value['type']);
                    node.append(input);
                    node.append($('<span/>').text(value['text']));

                    if (this.get_option(key)) {
                        input.attr('checked', 'checked');
                    }
                    input.change(function() {
                        that.set_option(key, !!this.checked);
                    });
                    container.append(node);
                }
            }
            return container;
		}
	}

	return {
		OptionDict: OptionDict
	}

});