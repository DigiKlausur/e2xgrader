define([
	'base/js/namespace'
], function(Jupyter) {
	return {
		remap: function() {
			console.log('Rebinding of keyboard shortcuts.!');

			let shortcuts = ['x', 'c', 'v', 'a', 'b', 'shift-v',
							 'shift-m', 'y', 'm', 'r', 'shift-enter', 'alt-enter',
							 'ctrl-shift-f', 'ctrl-shift-p', 'p', 'd,d'];

			// Remove shortcuts in command mode
			for (let i in shortcuts) {
				try {
					Jupyter.keyboard_manager.command_shortcuts.remove_shortcut(shortcuts[i]);

				} catch(e) {
					console.log('Command shortcut ' + shortcuts[i] + ' does not exist.');
				}
			}

			// Remove shortcuts in edit mode
			for (let i in shortcuts) {
				try {
					Jupyter.keyboard_manager.edit_shortcuts.remove_shortcut(shortcuts[i]);

				} catch(e) {
					console.log('Edit shortcut ' + shortcuts[i] + ' does not exist.');
				}
			}

			try {
				Jupyter.keyboard_manager.command_shortcuts.remove_shortcut('ctrl-v');

			} catch(e) {
				console.log('Command shortcut ' + 'ctrl-v' + ' does not exist.');
			}

			// Bind all execute cell shortcuts to run cell
			
			Jupyter.keyboard_manager.command_shortcuts.add_shortcut('alt-enter', {
				help : 'run cell',
				help_index : 'zz',
				handler : function (event) {
					IPython.notebook.execute_cell();
					return false;
				}}
			)

			Jupyter.keyboard_manager.command_shortcuts.add_shortcut('shift-enter', {
				help : 'run cell',
				help_index : 'zz',
				handler : function (event) {
					IPython.notebook.execute_cell();
					return false;
				}}
			)

			Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('alt-enter', {
				help : 'run cell',
				help_index : 'zz',
				handler : function (event) {
					IPython.notebook.execute_cell();
					return false;
				}}
			)

			Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('shift-enter', {
				help : 'run cell',
				help_index : 'zz',
				handler : function (event) {
					IPython.notebook.execute_cell();
					return false;
				}}
			)

			Jupyter.keyboard_manager.command_shortcuts.add_shortcut('ctrl-v', {
				help : 'no action',
				help_index : 'zz',
				handler : function (event) {
					return false;
				}}
			)

			console.log('Rebinding of keyboard shortcuts done!');
		}
	}
});