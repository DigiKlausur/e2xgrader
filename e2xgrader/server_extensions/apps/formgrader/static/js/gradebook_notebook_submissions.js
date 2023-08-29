let SubmittedNotebook = Backbone.Model.extend({});
let SubmittedNotebooks = Backbone.Collection.extend({
  model: SubmittedNotebook,
  url:
    base_url +
    "/formgrader/api/submitted_" +
    view +
    "s/" +
    assignment_id +
    "/" +
    notebook_id +
    task_id,
});

let SubmittedNotebookUI = Backbone.View.extend({
  events: {},

  initialize: function () {
    this.$reveal = this.$el.find(".reveal");
    this.$name = this.$el.find(".name");
    this.$score = this.$el.find(".score");
    this.$code_score = this.$el.find(".code-score");
    this.$written_score = this.$el.find(".written-score");
    this.$task_score = this.$el.find(".task-score");
    this.$needs_manual_grade = this.$el.find(".needs-manual-grade");
    this.$tests_failed = this.$el.find(".tests-failed");
    this.$flagged = this.$el.find(".flagged");
  },

  clear: function () {
    this.$reveal.empty();
    this.$name.empty();
    this.$score.empty();
    this.$code_score.empty();
    this.$written_score.empty();
    this.$task_score.empty();
    this.$needs_manual_grade.empty();
    this.$tests_failed.empty();
    this.$flagged.empty();
  },

  showName: function () {
    this.$reveal.parent().find(".name-shown").show();
    this.$reveal.parent().find(".name-hidden").hide();
  },

  hideName: function () {
    this.$reveal.parent().find(".name-hidden").show();
    this.$reveal.parent().find(".name-shown").hide();
  },

  render: function () {
    this.clear();
    // show/hide real name
    this.$reveal.append(
      $("<span/>")
        .addClass("glyphicon glyphicon-eye-open name-hidden")
        .attr("aria-hidden", "true")
        .on("click", _.bind(this.showName, this))
    );
    this.$reveal.append(
      $("<span/>")
        .addClass("glyphicon glyphicon-eye-close name-shown")
        .attr("aria-hidden", "true")
        .on("click", _.bind(this.hideName, this))
    );

    // notebook name
    let last_name = this.model.get("last_name");
    let first_name = this.model.get("first_name");
    let name = this.model.get("student");
    if (last_name !== null && first_name !== null) {
      name = last_name + ", " + first_name;
    }
    this.$name.attr("data-order", this.model.get("index"));
    this.$name.append(
      $("<a/>")
        .addClass("name-hidden")
        .attr(
          "href",
          base_url +
            "/formgrader/submissions/" +
            this.model.get("id") +
            "/?task=" +
            task_id.substr(1)
        )
        .text("Submission #" + (this.model.get("index") + 1))
    );
    this.$name.append(
      $("<a/>")
        .addClass("name-shown")
        .attr(
          "href",
          base_url +
            "/formgrader/submissions/" +
            this.model.get("id") +
            "/?task=" +
            task_id.substr(1)
        )
        .text(name)
    );

    // score
    let score = roundToPrecision(this.model.get("score"), 2);
    let max_score = roundToPrecision(this.model.get("max_score"), 2);
    if (max_score === 0) {
      this.$score.attr("data-order", 0.0);
    } else {
      this.$score.attr("data-order", score / max_score);
    }
    this.$score.text(score + " / " + max_score);

    if (view !== "task") {
      // code score
      score = roundToPrecision(this.model.get("code_score"), 2);
      max_score = roundToPrecision(this.model.get("max_code_score"), 2);
      if (max_score === 0) {
        this.$code_score.attr("data-order", 0.0);
      } else {
        this.$code_score.attr("data-order", score / max_score);
      }
      this.$code_score.text(score + " / " + max_score);

      // written score
      score = roundToPrecision(this.model.get("written_score"), 2);
      max_score = roundToPrecision(this.model.get("max_written_score"), 2);
      if (max_score === 0) {
        this.$written_score.attr("data-order", 0.0);
      } else {
        this.$written_score.attr("data-order", score / max_score);
      }
      this.$written_score.text(score + " / " + max_score);

      // task score
      score = roundToPrecision(this.model.get("task_score"), 2);
      max_score = roundToPrecision(this.model.get("max_task_score"), 2);
      if (max_score === 0) {
        this.$task_score.attr("data-order", 0.0);
      } else {
        this.$task_score.attr("data-order", score / max_score);
      }
      this.$task_score.text(score + " / " + max_score);
    }
    // needs manual grade?
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

    // tests failed?
    if (this.model.get("failed_tests")) {
      this.$tests_failed.attr("data-search", "tests failed");
      this.$tests_failed.attr("data-order", 1);
      this.$tests_failed.append(
        $("<span/>").addClass("glyphicon glyphicon-ok")
      );
    } else {
      this.$tests_failed.attr("data-search", "");
      this.$tests_failed.attr("data-order", 0);
    }

    // flagged?
    if (this.model.get("flagged")) {
      this.$flagged.attr("data-search", "flagged");
      this.$flagged.attr("data-order", 1);
      this.$flagged.append($("<span/>").addClass("glyphicon glyphicon-flag"));
    } else {
      this.$flagged.attr("data-search", "");
      this.$flagged.attr("data-order", 0);
    }
  },
});

let insertRow = function (table) {
  let row = $("<tr/>");
  row.append($("<td/>").addClass("reveal"));
  row.append($("<td/>").addClass("name"));
  row.append($("<td/>").addClass("text-center score"));
  row.append($("<td/>").addClass("text-center code-score"));
  row.append($("<td/>").addClass("text-center written-score"));
  row.append($("<td/>").addClass("text-center task-score"));
  row.append($("<td/>").addClass("text-center needs-manual-grade"));
  row.append($("<td/>").addClass("text-center tests-failed"));
  row.append($("<td/>").addClass("text-center flagged"));
  table.append(row);
  return row;
};

let loadSubmittedNotebooks = function () {
  let tbl = $("#main-table");

  const models = new SubmittedNotebooks();

  models.loaded = false;
  models.fetch({
    success: function () {
      tbl.empty();
      models.each(function (model) {
        let ui = new SubmittedNotebookUI({
          model: model,
          el: insertRow(tbl),
        });
        ui.render();
      });
      if (view === "task") {
        // Hide unused columns
        $("th:nth-child(4)").hide();
        $("th:nth-child(5)").hide();
        $("th:nth-child(6)").hide();
        $("td:nth-child(4)").hide();
        $("td:nth-child(5)").hide();
        $("td:nth-child(6)").hide();
      }
      insertDataTable(tbl.parent());
      $("span.glyphicon.name-hidden").tooltip({ title: "Show student name" });
      $("span.glyphicon.name-shown").tooltip({ title: "Hide student name" });
      models.loaded = true;
    },
  });
};

$(window).on("load", function () {
  loadSubmittedNotebooks();
});
