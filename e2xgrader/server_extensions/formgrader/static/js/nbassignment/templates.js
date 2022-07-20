let TemplateUI = BaseUI.extend({
  events: {},

  initialize: function () {
    this.$template_name = this.$el.find(".template-name");
    this.$edit_template = this.$el.find(".edit-template");
    this.$remove_template = this.$el.find(".remove-template");

    this.fields = [
      this.$template_name,
      this.$edit_template,
      this.$remove_template,
    ];

    this.listenTo(this.model, "sync", this.render);
    this.render();
  },

  render: function () {
    this.clear();
    let name = this.model.get("name");

    this.$template_name.append(
      $("<a/>")
        .attr("href", tree_url + "templates/" + name)
        .text(name)
    );
    this.$edit_template.append(
      $("<a/>")
        .attr(
          "href",
          notebook_url + "templates/" + name + "/" + name + ".ipynb"
        )
        .text("Edit")
    );
    this.$remove_template.append(
      $("<a/>")
        .attr("href", "#")
        .click(_.bind(this.removeTemplateModal, this))
        .append($("<span/>").text("Remove"))
    );
  },

  removeTemplateModal: function () {
    let body = $("<div/>");
    body.append(
      $("<p/>").text("Are you sure you want to delete the template?")
    );
    body.append($("<p/>").text("This action can't be undone!"));

    this.openRemoveModal(
      body,
      "Delete template " + this.model.get("name") + "?"
    );
  },
});

function addView(model, table) {
  let row = insertRow(table, [
    "template-name",
    "edit-template",
    "remove-template",
  ]);
  return new TemplateUI({
    model: model,
    el: row,
  });
}

function loadTemplates() {
  let tbl = $("#main_table");
  models = new Templates();
  models.loaded = false;
  models.fetch({
    success: function () {
      tbl.empty();
      models.each((model) => addView(model, tbl));
      dataTable = tbl.parent().DataTable({
        columnDefs: [
          { orderable: false, targets: [-1, -2] },
          { searchable: false, targets: [-1, -2] },
        ],
      });

      models.loaded = true;
    },
  });
}

function newTemplate() {
  let elem = getNewModalElements("Template");

  let $modal = createModal(
    "new-template-modal",
    "Create a new exercise template",
    elem.body,
    elem.footer
  );

  let $modal_save = $modal.find("button.save");
  $modal_save.click(function () {
    let $modal_name = $modal.find("input.modal-name").val();
    let template = new Template();
    template.save(
      {
        name: $modal_name,
        tasks: 0,
      },
      {
        success: function (template) {
          if (template.get("success")) {
            $modal.modal("hide");
            let row = addView(template, $("#main_table")).el;
            dataTable.row.add(row).draw();
            models.add([template]);
            window.location.href =
              notebook_url +
              "templates/" +
              $modal_name +
              "/" +
              $modal_name +
              ".ipynb";
          } else {
            createLogModal(
              "error-modal",
              "Error",
              "There was an error creating the template " +
                template.get("name") +
                "!",
              template.get("error")
            );
          }
        },
      }
    );
  });
}

let models = undefined;
let dataTable = undefined;

$(window).on("load", function () {
  loadTemplates();
});
