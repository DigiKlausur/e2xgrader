let PoolUI = BaseUI.extend({

    events: {},

    initialize: function () {
        this.$pool_name = this.$el.find('.pool-name');
        this.$number_of_tasks = this.$el.find('.number-of-tasks');
        this.$remove_pool = this.$el.find('.remove-pool');

        this.fields = [this.$pool_name, this.$number_of_tasks, this.$remove_pool];

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        this.clear();
        let name = this.model.get('name');
        
        this.$pool_name.append($('<a/>')
            .attr('href', base_url + '/taskcreator/pools/' + name)
            .text(name));
        this.$number_of_tasks.text(this.model.get('tasks'));
        this.$remove_pool.append($('<a/>')
            .attr('href', '#')
            .click(_.bind(this.removePoolModal, this))
            .append($('<span/>').text('Remove')
                ));
    },

    removePoolModal: function() {
        let body = $('<div/>');
        body.append($('<p/>').text('Are you sure you want to delete the task pool?'));
        body.append($('<p/>').text('It contains ' + this.model.get('tasks') + ' tasks that will be deleted!'));
        body.append($('<p/>').text('This action can\'t be undone!'));

        this.openRemoveModal(body, "Delete pool " + this.model.get('name') + "?");
    },

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('pool-name'));
    row.append($('<td/>').addClass('number-of-tasks'));
    row.append($('<td/>').addClass('remove-pool'));
    table.append(row);
    return row;
}

function addView(model, table) {
    let row = insertRow(table);

    return new PoolUI({
        'model': model,
        'el': row
    });
}

function loadPools() {
    let tbl = $('#main_table');
    models = new Pools();
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();            
            models.each((model) => addView(model, tbl));
            dataTable = tbl.parent().DataTable({
                'columnDefs': [
                    {'orderable': false, 'targets': [-1]},
                    {'searchable': false, 'targets': [-1]}
                ]
            });
            models.loaded = true;
        }
    });
}

function newPool() {
    let body = $('<div/>').append($('</p>').text(
        `Please specify the name of the new pool. Names can consist of characters, 
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
        .text('Add Task Pool'));
    footer.append($('<button/>')
        .addClass('btn btn-danger')
        .attr('data-dismiss', 'modal')
        .text('Cancel'));

    let $modal = createModal("new-pool-modal", "Create a new task pool", body, footer);
    
    let $modal_save = $modal.find('button.save');
    $modal_save.click(function () {
        let $modal_name = $modal.find('input.modal-name').val();
        let pool = new Pool();
        pool.save({
            'name': $modal_name,
            'tasks': 0
        }, {
            success: function(pool) {
            if (pool.get('success')) {
                $modal.modal('hide');
                let row = addView(pool, $('#main_table')).el;
                dataTable.row.add(row).draw();
                models.add([pool]);
            } else {
                createLogModal(
                    'error-modal',
                    'Error',
                    'There was an error creating the pool ' + pool.get('name') + '!',                    
                    pool.get('error'));
            }
        }});
    })

}

let models = undefined;
let dataTable = undefined;

$(window).on('load', function () {
    loadPools();
});
