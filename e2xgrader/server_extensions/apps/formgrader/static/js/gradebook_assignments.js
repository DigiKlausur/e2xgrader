let Assignment = Backbone.Model.extend({});
let Assignments = Backbone.Collection.extend({
  model: Assignment,
  url: base_url + "/formgrader/api/assignments",
});

let AssignmentUI = Backbone.View.extend({
  events: {},

  initialize: function () {
    this.$name = this.$el.find(".name");
    this.$duedate = this.$el.find(".duedate");
    this.$num_submissions = this.$el.find(".num-submissions");
    this.$score = this.$el.find(".score");
  },

  clear: function () {
    this.$name.empty();
    this.$duedate.empty();
    this.$num_submissions.empty();
    this.$score.empty();
  },

  render: function () {
    this.clear();

    // assignment name
    let name = this.model.get("name");
    this.$name.attr("data-order", name);
    this.$name.append(
      $("<a/>")
        .attr(
          "href",
          base_url + "/formgrader/gradebook/" + name + "/?view=" + view
        )
        .text(name)
    );

    // duedate
    let duedate = this.model.get("duedate");
    let display_duedate = this.model.get("display_duedate");
    if (duedate === null) {
      duedate = "None";
      display_duedate = "None";
    }
    this.$duedate.attr("data-order", duedate);
    this.$duedate.text(display_duedate);

    // number of submissions
    let num_submissions = this.model.get("num_submissions");
    this.$num_submissions.attr("data-order", num_submissions);
    this.$num_submissions.text(num_submissions);

    // score
    let score = roundToPrecision(this.model.get("average_score"), 2);
    let max_score = roundToPrecision(this.model.get("max_score"), 2);
    if (max_score === 0) {
      this.$score.attr("data-order", 0.0);
    } else {
      this.$score.attr("data-order", score / max_score);
    }
    this.$score.text(score + " / " + max_score);
  },
});

let insertRow = function (table) {
  let row = $("<tr/>");
  row.append($("<td/>").addClass("name"));
  row.append($("<td/>").addClass("text-center duedate"));
  row.append($("<td/>").addClass("text-center num-submissions"));
  row.append($("<td/>").addClass("text-center score"));
  table.append(row);
  return row;
};

let loadAssignments = function () {
  let tbl = $("#main-table");

  const models = new Assignments();
  models.loaded = false;
  models.fetch({
    success: function () {
      tbl.empty();
      models.each(function (model) {
        let ui = new AssignmentUI({
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
  loadAssignments();
});
