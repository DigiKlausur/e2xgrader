let ExerciseUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$exercise_name = this.$el.find('.exercise-name');
        this.$remove_exercise = this.$el.find('.remove-exercise');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        //this.$exercise_name.text(name);
        this.$exercise_name.append($('<a/>')
            .attr('href', base_url + '/taskcreator/exercises/' + name)
            .text(name));
        this.$remove_exercise.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/exercise/' + name)
            .text('Remove'));
    }

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('exercise-name'));
    row.append($('<td/>').addClass('remove-exercise'));
    table.append(row);
    return row;
}

function loadExercises() {
    console.log('Loading the exercises');
    let tbl = $('#main_table');
    models = new Exercises({assignment: assignment});
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                let view = new ExerciseUI({
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
    loadExercises();
})
