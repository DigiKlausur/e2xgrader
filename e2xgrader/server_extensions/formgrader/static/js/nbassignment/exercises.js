let ExerciseUI = BaseUI.extend({

    events: {},

    initialize: function () {
        this.$exercise_name = this.$el.find('.exercise-name');
        this.$remove_exercise = this.$el.find('.remove-exercise');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        this.$exercise_name.append($('<a/>')
            .attr('href', notebook_url + 'source/' + assignment + '/' + name + '.ipynb')
            .text(name));
        
        this.$remove_exercise.append($('<a/>')
            .attr('href', '#')
            .click(_.bind(this.removeExerciseModal, this))
            .append($('<span/>').text('Remove')
                ));
    },
    
    removeExerciseModal: function() {
        let body = $('<div/>');
        body.append($('<p/>').text('Are you sure you want to delete the exercise?'));
        body.append($('<p/>').text('This action can\'t be undone!'));

        this.openRemoveModal(body, "Delete exercise " + this.model.get('name') + "?");
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
                console.log(model);
                let view = new ExerciseUI({
                    'model': model,
                    'el': insertRow(tbl)
                });
                views.push(view);
            });
            dataTable = tbl.parent().DataTable();

            models.loaded = true;
        }
    })

}

let models = undefined;
let views = [];
let dataTable = undefined;

$(window).on('load', function () {
    loadExercises();
})
