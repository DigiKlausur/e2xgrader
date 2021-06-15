let Task = Backbone.Model.extend({
    idAttribute: 'name',
    urlRoot: base_url + '/taskcreator/api/task'
});

let Tasks = Backbone.Collection.extend({
    model: Task,
    url: base_url + '/taskcreator/api/pools/' + pool
});

let TaskUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$task_name = this.$el.find('.task-name');
        this.$number_of_questions = this.$el.find('.number-of-questions');
        this.$points = this.$el.find('.points');
        this.$edit_task = this.$el.find('.edit-task');
        this.$remove_task = this.$el.find('.remove-task');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        //this.$task_name.text(name);
        this.$task_name.append($('<a/>')
            .attr('href', base_url + '/tree/pools/' + pool + '/' + name)
            .text(name));
        this.$points.text(this.model.get('points'));
        this.$number_of_questions.text(this.model.get('questions'));
        this.$edit_task.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/task/' + name)
            .text('Edit'));
        this.$remove_task.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/task/' + name)
            .text('Remove'));
    }

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('task-name'));
    row.append($('<td/>').addClass('number-of-questions'));
    row.append($('<td/>').addClass('points'));
    row.append($('<td/>').addClass('edit-task'));
    row.append($('<td/>').addClass('remove-task'));
    table.append(row);
    return row;
}

function loadTasks() {
    console.log('Loading the tasks');
    let tbl = $('#task_table');
    models = new Tasks();
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                let view = new TaskUI({
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
    loadTasks();
})
