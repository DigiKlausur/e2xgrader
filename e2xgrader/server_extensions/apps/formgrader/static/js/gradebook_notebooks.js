let Notebook = Backbone.Model.extend({});
let Notebooks = Backbone.Collection.extend({
  model: Notebook,
  url: base_url + "/formgrader/api/notebooks/" + assignment_id,
});

let NotebookUI = Backbone.View.extend({
  events: {},

  initialize: function () {
    this.$name = this.$el.find(".name");
    this.$avg_score = this.$el.find(".avg-score");
    this.$avg_code_score = this.$el.find(".avg-code-score");
    this.$avg_written_score = this.$el.find(".avg-written-score");
    this.$avg_task_score = this.$el.find(".avg-task-score");
    this.$needs_manual_grade = this.$el.find(".needs-manual-grade");
  },

  clear: function () {
    this.$name.empty();
    this.$avg_score.empty();
    this.$avg_code_score.empty();
    this.$avg_written_score.empty();
    this.$avg_task_score.empty();
    this.$needs_manual_grade.empty();
  },

  render: function () {
    this.clear();

    // notebook name
    let name = this.model.get("name");
    this.$name.attr("data-order", name);
    if (view === "task") {
      this.$name.append(
        $("<a/>")
          .attr(
            "href",
            base_url +
              "/formgrader/gradebook/tasks/" +
              assignment_id +
              "/" +
              name
          )
          .text(name)
      );
    } else {
      this.$name.append(
        $("<a/>")
          .attr(
            "href",
            base_url + "/formgrader/gradebook/" + assignment_id + "/" + name
          )
          .text(name)
      );
    }

    // average score
    let score = roundToPrecision(this.model.get("average_score"), 2);
    let max_score = roundToPrecision(this.model.get("max_score"), 2);
    if (max_score === 0) {
      this.$avg_score.attr("data-order", 0.0);
    } else {
      this.$avg_score.attr("data-order", score / max_score);
    }
    this.$avg_score.text(score + " / " + max_score);

    // average code score
    score = roundToPrecision(this.model.get("average_code_score"), 2);
    max_score = roundToPrecision(this.model.get("max_code_score"), 2);
    if (max_score === 0) {
      this.$avg_code_score.attr("data-order", 0.0);
    } else {
      this.$avg_code_score.attr("data-order", score / max_score);
    }
    this.$avg_code_score.text(score + " / " + max_score);

    // average written score
    score = roundToPrecision(this.model.get("average_written_score"), 2);
    max_score = roundToPrecision(this.model.get("max_written_score"), 2);
    if (max_score === 0) {
      this.$avg_written_score.attr("data-order", 0.0);
    } else {
      this.$avg_written_score.attr("data-order", score / max_score);
    }
    this.$avg_written_score.text(score + " / " + max_score);

    // average task score
    score = roundToPrecision(this.model.get("average_task_score"), 2);
    max_score = roundToPrecision(this.model.get("max_task_score"), 2);
    if (max_score === 0) {
      this.$avg_task_score.attr("data-order", 0.0);
    } else {
      this.$avg_task_score.attr("data-order", score / max_score);
    }
    this.$avg_task_score.text(score + " / " + max_score);

    // needs manual grade
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
  row.append($("<td/>").addClass("text-center avg-code-score"));
  row.append($("<td/>").addClass("text-center avg-written-score"));
  row.append($("<td/>").addClass("text-center avg-task-score"));
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
