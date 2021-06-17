let Assignment = Backbone.Model.extend({
    idAttribute: 'name',
    urlRoot: base_url + '/taskcreator/api/assignment'
});

let Assignments = Backbone.Collection.extend({
    model: Assignment,
    url: base_url + '/taskcreator/api/assignments'
});

let AssignmentUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$assignment_name = this.$el.find('.assignment-name');
        this.$number_of_exercises = this.$el.find('.number-of-exercises');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        //this.$assignment_name.text(name);
        this.$assignment_name.append($('<a/>')
            .attr('href', base_url + '/taskcreator/assignments/' + name)
            .text(name));
        this.$number_of_exercises.text(this.model.get('exercises'));
    }

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('assignment-name'));
    row.append($('<td/>').addClass('number-of-exercises'));
    table.append(row);
    return row;
}

function loadAssignments() {
    console.log('Loading the assignments');
    let tbl = $('#main_table');
    models = new Assignments();
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                let view = new AssignmentUI({
                    'model': model,
                    'el': insertRow(tbl)
                });
                views.push(view);
            });
            //insertDataTable(tbl.parent());
            tbl.parent().DataTable();

            models.loaded = true;
        }
    })

}

let models = undefined;
let views = [];

$(window).on('load', function () {
    loadAssignments();
})
