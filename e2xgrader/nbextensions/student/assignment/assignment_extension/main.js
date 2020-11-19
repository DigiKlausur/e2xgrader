define([
    'base/js/namespace',
    'base/js/events',
    './model/nbgrader_model',
    './assignment_notebook',
    './assignment_view'
], function (Jupyter, events, model, assignment_notebook, assignment_view) {

    "use strict";

    function initialize() {
        if (!model.is_assignment_notebook()) {
            return;
        }
        assignment_view.initialize();
        assignment_notebook.initialize();
    }

    function load_ipython_extension() {
        if (Jupyter.notebook && Jupyter.notebook._fully_loaded) {
            initialize();
        } else {
            events.one('notebook_loaded.Notebook', initialize);
        }
    }

    return {
        load_ipython_extension: load_ipython_extension
    }
})