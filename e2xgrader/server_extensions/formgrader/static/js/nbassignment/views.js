let BaseUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.fields = [];
    },

    clear: function () {
        this.fields.forEach((field) => field.empty());
    },

    openRemoveModal: function(body, title) {
        let footer = $('<div/>');
        footer.append($('<button/>')
            .addClass('btn btn-danger save')
            .text('Delete'));
        footer.append($('<button/>')
            .addClass('btn ')
            .attr('data-dismiss', 'modal')
            .text('Cancel'));

        $modal = createModal("remove-pool-modal", title, body, footer);
        $modal_save = $modal.find('button.save');
        let that = this;
        $modal_save.click(function () {
            that.removeModel();
            $modal.modal('hide');
        });
    },

    removeModel: function () {
        this.model.destroy();
        this.remove();
        console.log(this.$el)
        dataTable.row(this.$el).remove().draw();
    }
});

/*
let PoolUI = BaseUI.extend({

    events: {},

    initialize: function () {
        this.$pool_name = this.$el.find('.pool-name');
        this.$number_of_tasks = this.$el.find('.number-of-tasks');
        this.$edit_pool = this.$el.find('.edit-pool');
        this.$remove_pool = this.$el.find('.remove-pool');

        this.fields = [this.$pool_name, this.$number_of_tasks, this.$edit_pool, this.$remove_pool];

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
        this.$edit_pool.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/pool/' + name)
            .text('Edit'));
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

});*/
