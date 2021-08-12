let TaskUI = BaseUI.extend({

    events: {},

    initialize: function () {
        this.$task_name = this.$el.find('.task-name');
        this.$number_of_questions = this.$el.find('.number-of-questions');
        this.$points = this.$el.find('.points');
        this.$edit_task = this.$el.find('.edit-task');
        this.$remove_task = this.$el.find('.remove-task');

        this.fields = [this.$task_name, this.$number_of_questions,
                       this.$points, this.$edit_task, this.$remove_task];

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        this.clear();
        let name = this.model.get('name');
        this.$task_name.append($('<a/>')
            .attr('href', tree_url + 'pools/' + pool + '/' + name)
            .text(name));
        this.$points.text(this.model.get('points'));
        this.$number_of_questions.text(this.model.get('questions'));
        this.$edit_task.append($('<a/>')
            .attr('href', notebook_url + 'pools/' + pool + '/' + name + '/' + name + '.ipynb')
            .text('Edit'));
        this.$remove_task.append($('<a/>')
            .attr('href', '#')
            .click(_.bind(this.removeTaskModal, this))
            .append($('<span/>').text('Remove')
                ));
    },

    removeTaskModal: function() {
        let body = $('<div/>');
        body.append($('<p/>').text('Are you sure you want to delete the task?'));
        body.append($('<p/>').text('This action can\'t be undone!'));

        this.openRemoveModal(body, "Delete task " + this.model.get('name') + "?");
    },

});

function addView(model, table) {
    let row = insertRow(table, ['task-name', 'number-of-questions', 'points', 'edit-task', 'remove-task']);
    return new TaskUI({
        'model': model,
        'el': row
    });
}

function loadTasks() {
    let tbl = $('#main_table');
    models = new Tasks({pool: pool});
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();

            models.each((model) => addView(model, tbl));
            dataTable = tbl.parent().DataTable({
                'columnDefs': [
                    {'orderable': false, 'targets': [-1, -2]},
                    {'searchable': false, 'targets': [-1, -2]}
                ]
            });
            models.loaded = true;
        }
    })

}

function newTask() {
    let body = $('<div/>').append($('</p>').text(
        `Please specify the name of the new task. Names can consist of characters,
         digits, spaces and underscores.`));
    let table = $('<table/>').addClass('table table-striped form-table');
    let tablebody = $('<tbody/>');
    body.append(table);
    table.append(tablebody);
    let name = $('<tr/>');
    tablebody.append(name);
    name.append($('<td/>').addClass('align-middle').text('Name'));
    name.append($('<td/>').append($('<input/>')
        .addClass('modal-name')
        .attr('pattern', '[A-Za-z0-9]+')
        .attr('type', 'text')));
    let footer = $('<div/>');
    footer.append($('<button/>')
        .addClass('btn btn-primary save')
        .text('Add Task'));
    footer.append($('<button/>')
        .addClass('btn btn-danger')
        .attr('data-dismiss', 'modal')
        .text('Cancel'));

    let $modal = createModal("new-task-modal", "Create a new task", body, footer);

    let $modal_save = $modal.find('button.save');
    $modal_save.click(function () {
        let $modal_name = $modal.find('input.modal-name').val();
        let task = new Task({
            pool: pool,
            name: $modal_name,
        });

        task.save(undefined, {
            success: function () {
                if (task.get('success')) {
                    task.fetch({
                        success: function () {
                            $modal.modal('hide');
                            let row = addView(task, $('#main_table')).el;
                            dataTable.row.add(row).draw();
                            models.add([task]);
                            window.location.href= notebook_url + 'pools/' + pool + '/' + $modal_name + '/' + $modal_name + '.ipynb';
                        }
                    });
                } else {
                    createLogModal(
                        'error-modal',
                        'Error',
                        'There was an error creating the task ' + task.get('name') + '!',
                        task.get('error'));
                }
            }
        });
    });
}

let models = undefined;
let dataTable = undefined;

$(window).on('load', function () {
    loadTasks();
})
