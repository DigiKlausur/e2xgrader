let Pool = Backbone.Model.extend({
    idAttribute: 'name',
    urlRoot: base_url + '/taskcreator/api/pool'
});

let Pools = Backbone.Collection.extend({
    model: Pool,
    url: base_url + '/taskcreator/api/pools/'
});

let PoolUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$pool_name = this.$el.find('.pool-name');
        this.$number_of_tasks = this.$el.find('.number-of-tasks');
        this.$edit_pool = this.$el.find('.edit-pool');
        this.$remove_pool = this.$el.find('.remove-pool');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        //this.$pool_name.text(name);
        this.$pool_name.append($('<a/>')
            .attr('href', base_url + '/taskcreator/pools/' + name)
            .text(name));
        this.$number_of_tasks.text(this.model.get('tasks'));
        this.$edit_pool.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/pool/' + name)
            .text('Edit'));
        this.$remove_pool.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/pool/' + name)
            .text('Remove'));
    }

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('pool-name'));
    row.append($('<td/>').addClass('number-of-tasks'));
    row.append($('<td/>').addClass('edit-pool'));
    row.append($('<td/>').addClass('remove-pool'));
    table.append(row);
    return row;
}

function loadPools() {
    console.log('Loading the pools');
    let tbl = $('#pool_table');
    models = new Pools();
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                let view = new PoolUI({
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
    loadPools();
})
