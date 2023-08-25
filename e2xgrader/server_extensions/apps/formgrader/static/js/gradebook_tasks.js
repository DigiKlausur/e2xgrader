let Notebook = Backbone.Model.extend({});
let Notebooks = Backbone.Collection.extend({
  model: Notebook,
  url:
    base_url +
    "/formgrader/api/solution_cells/" +
    assignment_id +
    "/" +
    notebook_id,
});

let NotebookUI = Backbone.View.extend({
  events: {},

  initialize: function () {
    this.$name = this.$el.find(".name");
    this.$avg_score = this.$el.find(".avg-score");
    this.$autograded = this.$el.find(".autograded");
    this.$needs_manual_grade = this.$el.find(".needs-manual-grade");
  },

  clear: function () {
    this.$name.empty();
    this.$avg_score.empty();
    this.$autograded.empty();
    this.$needs_manual_grade.empty();
  },

  render: function () {
    this.clear();

    // notebook name
    let name = this.model.get("name");
    this.$name.attr("data-order", name);
    this.$name.append(
      $("<a/>")
        .attr(
          "href",
          base_url +
            "/formgrader/gradebook/" +
            assignment_id +
            "/" +
            notebook_id +
            "/?view=task&filter=" +
            name
        )
        .text(name)
    );

    // average score

    let score = roundToPrecision(this.model.get("avg_score"), 2);
    let max_score = roundToPrecision(this.model.get("max_score"), 2);
    if (max_score === 0) {
      this.$avg_score.attr("data-order", 0.0);
    } else {
      this.$avg_score.attr("data-order", score / max_score);
    }
    this.$avg_score.text(score + " / " + max_score);

    if (this.model.get("autograded")) {
      this.$autograded.attr("data-search", "autograded task");
      this.$autograded.attr("data-order", 1);
      this.$autograded.append($("<span/>").addClass("glyphicon glyphicon-ok"));
    } else {
      this.$autograded.attr("data-search", "");
      this.$autograded.attr("data-order", 0);
    }

    if (this.model.get("needs_manual_grade")) {
      this.$needs_manual_grade.attr("data-search", "needs manual grade");
      this.$needs_manual_grade.attr("data-order", 1);
      this.$needs_manual_grade.append(
        $("<span/>").addClass("glyphicon glyphicon-ok")
      );
    } else {
      this.$needs_manual_grade.attr("data-search", "");
      this.$needs_manual_grade.attr("data-order", 0);
    }
  },
});

let insertRow = function (table) {
  let row = $("<tr/>");
  row.append($("<td/>").addClass("name"));
  row.append($("<td/>").addClass("text-center avg-score"));
  row.append($("<td/>").addClass("text-center autograded"));
  row.append($("<td/>").addClass("text-center needs-manual-grade"));
  table.append(row);
  return row;
};

let loadNotebooks = function () {
  let tbl = $("#main-table");

  const models = new Notebooks();
  models.loaded = false;
  models.fetch({
    success: function () {
      tbl.empty();
      models.each(function (model) {
        let ui = new NotebookUI({
          model: model,
          el: insertRow(tbl),
        });
        ui.render();
      });
      insertDataTable(tbl.parent());
      models.loaded = true;
    },
  });
};

$(window).on("load", function () {
  loadNotebooks();
});
