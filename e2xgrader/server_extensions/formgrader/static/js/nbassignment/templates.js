let Template = Backbone.Model.extend({
    idAttribute: 'name',
    urlRoot: base_url + '/taskcreator/api/template'
});

let Templates = Backbone.Collection.extend({
    model: Template,
    url: base_url + '/taskcreator/api/templates/'
});

let TemplateUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$template_name = this.$el.find('.template-name');
        this.$edit_template = this.$el.find('.edit-template');
        this.$remove_template = this.$el.find('.remove-template');

        this.listenTo(this.model, 'sync', this.render);
        this.render();
    },

    render: function () {
        let name = this.model.get('name');
        //this.$template_name.text(name);
        this.$template_name.append($('<a/>')
            .attr('href', base_url + '/tree/templates/' + name)
            .text(name));
        this.$edit_template.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/template/' + name)
            .text('Edit'));
        this.$remove_template.append($('<a/>')
            .attr('href', base_url + '/taskcreator/api/template/' + name)
            .text('Remove'));
    }

});

function insertRow(table) {
    let row = $('<tr/>');
    row.append($('<td/>').addClass('template-name'));
    row.append($('<td/>').addClass('edit-template'));
    row.append($('<td/>').addClass('remove-template'));
    table.append(row);
    return row;
}

function loadTemplates() {
    console.log('Loading the templates');
    let tbl = $('#template_table');
    models = new Templates();
    views = [];
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                let view = new TemplateUI({
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
    loadTemplates();
})
