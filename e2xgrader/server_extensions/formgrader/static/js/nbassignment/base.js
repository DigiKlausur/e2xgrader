let Assignment = Backbone.Model.extend({
  idAttribute: "name",
  urlRoot: base_url + "/taskcreator/api/assignment",
});

let Assignments = Backbone.Collection.extend({
  model: Assignment,
  url: base_url + "/taskcreator/api/assignments",
});

let Exercise = Backbone.Model.extend({
  idAttribute: "name",
  initialize: function (options) {
    this.urlRoot = base_url + "/taskcreator/api/exercise/" + options.assignment;
  },
});

let Exercises = Backbone.Collection.extend({
  model: Exercise,
  initialize: function (options) {
    this.url = base_url + "/taskcreator/api/assignments/" + options.assignment;
  },
});

let Pool = Backbone.Model.extend({
  idAttribute: "name",
  urlRoot: base_url + "/taskcreator/api/pool",
});

let Pools = Backbone.Collection.extend({
  model: Pool,
  url: base_url + "/taskcreator/api/pools/",
  comparator: "name",
});

let Task = Backbone.Model.extend({
  idAttribute: "name",
  initialize: function (options) {
    this.urlRoot = base_url + "/taskcreator/api/task/" + options.pool;
  },
});

let Tasks = Backbone.Collection.extend({
  model: Task,
  initialize: function (options) {
    this.url = base_url + "/taskcreator/api/pools/" + options.pool;
  },
  comparator: "name",
});

let Template = Backbone.Model.extend({
  idAttribute: "name",
  urlRoot: base_url + "/taskcreator/api/template",
});

let Templates = Backbone.Collection.extend({
  model: Template,
  url: base_url + "/taskcreator/api/templates/",
});

let BaseUI = Backbone.View.extend({
  events: {},

  initialize: function () {
    this.fields = [];
  },

  clear: function () {
    this.fields.forEach((field) => field.empty());
  },

  openRemoveModal: function (body, title) {
    let footer = $("<div/>");
    footer.append(
      $("<button/>").addClass("btn btn-danger save").text("Delete")
    );
    footer.append(
      $("<button/>")
        .addClass("btn ")
        .attr("data-dismiss", "modal")
        .text("Cancel")
    );

    let $modal = createModal("remove-pool-modal", title, body, footer);
    let $modal_save = $modal.find("button.save");
    let that = this;
    $modal_save.click(function () {
      that.removeModel();
      $modal.modal("hide");
    });
  },

  removeModel: function () {
    this.model.destroy();
    this.remove();
    console.log(this.$el);
    dataTable.row(this.$el).remove().draw();
  },
});

function insertRow(table, classes) {
  let row = $("<tr/>");
  classes.forEach(function (cls) {
    row.append($("<td/>").addClass(cls));
  });
  table.append(row);
  return row;
}

function getNewModalElements(element_name) {
  let body = $("<div/>").append(
    $("</p>").text(
      "Please specify the name of the new " +
        element_name.toLowerCase() +
        ". Names can consist of characters, digits, spaces and underscores."
    )
  );
  let table = $("<table/>").addClass("table table-striped form-table");
  let tablebody = $("<tbody/>");
  body.append(table);
  table.append(tablebody);
  let name = $("<tr/>");
  tablebody.append(name);
  name.append($("<td/>").addClass("align-middle").text("Name"));
  name.append(
    $("<td/>").append(
      $("<input/>")
        .addClass("modal-name")
        .attr("pattern", "[A-Za-z0-9]+")
        .attr("type", "text")
    )
  );
  let footer = $("<div/>");
  footer.append(
    $("<button/>")
      .addClass("btn btn-primary save")
      .text("Add " + element_name)
  );
  footer.append(
    $("<button/>")
      .addClass("btn btn-danger")
      .attr("data-dismiss", "modal")
      .text("Cancel")
  );
  return {
    body: body,
    footer: footer,
  };
}
