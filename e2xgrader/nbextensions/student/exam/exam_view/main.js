define([
    'require',
    'jquery',
    'base/js/namespace',
    'base/js/utils',
    './submit/submit',
    './remap_keys/remap_keybindings',
], function (require, $, Jupyter, utils, submit_tools, remap_keys) {

    'use strict';

    function remove_elements() {
        let elements = [
            '#insert_above_below',
            '#cut_copy_paste',
            '#move_up_down',
            '#cell_type',
            '#cmd_palette',
        ];

        elements.forEach(function (element) {
            $(element).remove();
        });

        $('#menubar').hide();
        $('.header-bar').hide();
        $('#notebook_name').hide();
    }

    function add_toolbar() {
        let div = $('<div/>').attr('id', 'e2xtoolbar');
        let name = Jupyter.notebook.notebook_name.split('.ipynb')[0];

        $('#save_widget').prepend(
            $('<span/>').text(name).attr('id', 'nb_name')
        );

        div.append($('<span/>').text('e²x').addClass('toolbarbutton'));

        let items = [
            $('#save-notbook'),
            $('#run_int'),
        ];

        items.forEach(function (item) {
            div.append(item);
        });

        
        
        let submit = new submit_tools.Submit();
        let submit_btn = $('<button/>')
            .attr('id', 'submit')
            .click(function() {
                console.log('Clicked on submit button');
                submit.prepare_submit()
            });
        submit_btn.append(
            $('<span/>').text('Submit')
        );
        submit_btn.append(
            $('<i/>').addClass('fa fa-paper-plane')
        );

        //submit_btn.hide();
        div.append(submit_btn);

        let help = $('<button/>')
            .attr('id', 'e2xhelp')
            .click(() => window.open(Jupyter.notebook.base_url + 'e2xhelp/base/html/en', '_blank'));
        help.append($('<span/>').text('Help'));
        help.append($('<i/>').addClass('fa fa-question'));
        div.append(help);

        let kernel_indicator = $('<span/>').attr('id', 'e2x_kernel_indicator')
            .append($('.kernel_indicator_name'))
            .append($('#kernel_indicator_icon'));

        div.append(kernel_indicator);

        div.append(advanced_options());
        div.insertAfter($('#maintoolbar-container'));
    }

    function advanced_options() {
        let open_menu = $('<span/>').addClass('e2xbutton').attr('id', 'advanced').append($('<a/>').append('Advanced'));

        let menu = $('<ul/>').addClass('dropdown');
        let options = [
            ['Clear All Outputs', () => Jupyter.notebook.clear_all_output()],
        ];

        options.forEach(function (option) {
            let li = $('<li/>').addClass('dropdown_item');
            li.append($('<a/>').append(option[0]));
            li.click(option[1]);
            menu.append(li);
        })

        open_menu.append(menu);
        return open_menu;
    }

    function load_css(file) {
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = require.toUrl('./' + file);
        document.getElementsByTagName("head")[0].appendChild(link);
    }

    function init() {
        load_css('examview.css');
        remove_elements();
        add_toolbar();
        remap_keys.remap();
    }

    function load_extension() {
        if (Jupyter.notebook) {
            init();
        } else {
            events.on('notebook_loaded.notebook', function () {
                init();
            })
        }
    }

    return {
        load_ipython_extension: load_extension
    }

});