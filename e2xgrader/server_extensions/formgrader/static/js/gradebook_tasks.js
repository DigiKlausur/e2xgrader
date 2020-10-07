var Notebook = Backbone.Model.extend({});
var Notebooks = Backbone.Collection.extend({
    model: Notebook,
    url: base_url + "/formgrader/api/solution_cells/" + assignment_id + "/" + notebook_id
});

var NotebookUI = Backbone.View.extend({

    events: {},

    initialize: function () {
        this.$name = this.$el.find(".name");
        this.$avg_score = this.$el.find(".avg-score");
        this.$autograded = this.$el.find(".autograded");
        this.$needs_manual_grade = this.$el.find(".needs-manual-grade");

        this.render();
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
        var name = this.model.get("name");
        this.$name.attr("data-order", name);
        this.$name.append($("<a/>")
            .attr("href", base_url + "/formgrader/gradebook/" + assignment_id + "/" + notebook_id + "/?view=task&filter=" + name)
            .text(name));

        // average score
        
        var score = roundToPrecision(this.model.get("avg_score"), 2);
        var max_score = roundToPrecision(this.model.get("max_score"), 2);
        if (max_score === 0) {
            this.$avg_score.attr("data-order", 0.0);
        } else {
            this.$avg_score.attr("data-order", score / max_score);
        }
        this.$avg_score.text(score + " / " + max_score);
        

        if (this.model.get("autograded")) {
            this.$autograded.attr("data-search", "autograded task");
            this.$autograded.attr("data-order", 1);
            this.$autograded.append($("<span/>")
                .addClass("glyphicon glyphicon-ok"));
        } else {
            this.$autograded.attr("data-search", "");
            this.$autograded.attr("data-order", 0);
        }
        
        
        if (this.model.get("needs_manual_grade")) {
            this.$needs_manual_grade.attr("data-search", "needs manual grade");
            this.$needs_manual_grade.attr("data-order", 1);
            this.$needs_manual_grade.append($("<span/>")
                .addClass("glyphicon glyphicon-ok"));
        } else {
            this.$needs_manual_grade.attr("data-search", "");
            this.$needs_manual_grade.attr("data-order", 0);
        }

    },
});

var insertRow = function (table) {
    var row = $("<tr/>");
    row.append($("<td/>").addClass("name"));
    row.append($("<td/>").addClass("text-center avg-score"));
    row.append($("<td/>").addClass("text-center autograded"));
    row.append($("<td/>").addClass("text-center needs-manual-grade"));
    table.append(row)
    return row;
};

var loadNotebooks = function () {
    var tbl = $("#main-table");

    models = new Notebooks();
    models.loaded = false;
    models.fetch({
        success: function () {
            tbl.empty();
            models.each(function (model) {
                var view = new NotebookUI({
                    "model": model,
                    "el": insertRow(tbl)
                });
            });
            insertDataTable(tbl.parent());
            models.loaded = true;
        }
    });
};

var models = undefined;

$(window).on('load', function () {
    loadNotebooks();
});
