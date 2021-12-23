var GradeUI = Backbone.View.extend({

    events: {
        "change .score": "save",
        "change .extra-credit": "save",
        "click .full-credit": "assignFullCredit",
        "click .no-credit": "assignNoCredit",
        "click .mark-graded": "save"
    },

    initialize: function () {
        this.$glyph = this.$el.find(".score-saved");
        this.$score = this.$el.find(".score");
        this.$extra_credit = this.$el.find(".extra-credit");
        this.$mark_graded = this.$el.find(".mark-graded");

        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model, "request", this.animateSaving);
        this.listenTo(this.model, "sync", this.animateSaved);

        this.$score.attr("placeholder", this.model.get("auto_score"));
        this.$extra_credit.attr("placeholder", 0.0);
        this.render();
    },

    render: function () {
        this.$score.val(this.model.get("manual_score"));
        this.$extra_credit.val(this.model.get("extra_credit"));
        if (this.model.get("needs_manual_grade")) {
            this.$score.addClass("needs_manual_grade");
            if (this.model.get("manual_score") !== null) {
                this.$mark_graded.show();
            }
        } else {
            this.$score.removeClass("needs_manual_grade");
            this.$mark_graded.hide();
        }
    },

    save: function () {
        var score, extra_credit;
        if (this.$score.val() === "") {
            score = null;
        } else {
            var val = this.$score.val();
            var max_score = this.model.get("max_score");
            if (val > max_score) {
                this.animateInvalidValue(this.$score);
                score = max_score;
            } else if (val < 0) {
                this.animateInvalidValue(this.$score);
                score = 0;
            } else {
                score = val;
            }
        }

        if (this.$extra_credit.val() == "") {
            extra_credit = null;
        } else {
            var val = this.$extra_credit.val();
            if (val < 0) {
                this.animateInvalidValue(this.$extra_credit);
                extra_credit = 0;
            } else {
                extra_credit = val;
            }
        }

        this.model.save({"manual_score": score, "extra_credit": extra_credit});
        this.render();
    },

    animateSaving: function () {
        this.$glyph.removeClass("glyphicon-ok");
        this.$glyph.addClass("glyphicon-refresh");
        this.$glyph.fadeIn(10);
    },

    animateSaved: function () {
        this.$glyph.removeClass("glyphicon-refresh");
        this.$glyph.addClass("glyphicon-ok");
        var that = this;
        setTimeout(function () {
            that.$glyph.fadeOut();
        }, 1000);
        $(document).trigger("finished_saving");
    },

    animateInvalidValue: function (elem) {
        var that = this;
        elem.animate({
            "background-color": "#FF8888",
            "border-color": "red"
        }, 100, undefined, function () {
            setTimeout(function () {
                elem.animate({
                    "background-color": "white",
                    "border-color": "white"
                }, 100);
            }, 50);
        });
    },

    assignFullCredit: function () {
        this.model.save({"manual_score": this.model.get("max_score")});
        this.$score.select();
        this.$score.focus();
    },

    assignNoCredit: function () {
        this.model.save({"manual_score": 0, "extra_credit": 0});
        this.$score.select();
        this.$score.focus();
    }
});

var Grade = Backbone.Model.extend({
    urlRoot: base_url + "/api/grade"
});

var Grades = Backbone.Collection.extend({
    model: Grade,
    url: base_url + "/api/grades"
});

var CommentUI = Backbone.View.extend({

    events: {
        "change .comment": "save",
    },

    initialize: function () {
        this.$glyph = this.$el.find(".comment-saved");
        this.$comment = this.$el.find(".comment");

        this.listenTo(this.model, "change", this.render);
        this.listenTo(this.model, "request", this.animateSaving);
        this.listenTo(this.model, "sync", this.animateSaved);

        var default_msg = "Type any comments here (supports Markdown and MathJax)";
        this.$comment.attr("placeholder", this.model.get("auto_comment") || default_msg);

        this.render();
        autosize(this.$comment);
    },

    render: function () {
        this.$comment.val(this.model.get("manual_comment"));
    },

    save: function () {
        this.model.save({"manual_comment": this.$comment.val()});
    },

    animateSaving: function () {
        this.$glyph.removeClass("glyphicon-ok");
        this.$glyph.addClass("glyphicon-refresh");
        this.$glyph.fadeIn(10);
    },

    animateSaved: function () {
        this.$glyph.removeClass("glyphicon-refresh");
        this.$glyph.addClass("glyphicon-ok");
        var that = this;
        setTimeout(function () {
            that.$glyph.fadeOut();
        }, 1000);
        $(document).trigger("finished_saving");
    },
});

var Comment = Backbone.Model.extend({
    urlRoot: base_url + "/api/comment"
});

var Comments = Backbone.Collection.extend({
    model: Comment,
    url: base_url + "/api/comments"
});

var AnnotationUI = Backbone.View.extend({

    initialize: function () {
        this.$canvas = this.$el.find(".annotationarea").get(0);
        this.$ctx = this.$canvas.getContext("2d");
        this.$edit_btn = this.$el.find(".annotate").get(0);
        $(this.$edit_btn).click(function () {
            alert('You sneaky dude clicked it!');
        })
        console.log(this.model.get('name'));

        this.render();
        this.initializePaint();

    },

    initializePaint: function () {
        this.drawing = false;
        this.edit_mode = true;
        this.position = null;
        this.shape = [];
        this.rect = this.$canvas.getBoundingClientRect();
        this.offsetHeight = this.$canvas.offsetHeight;
        this.offsetWidth = this.$canvas.offsetWidth;
        this.$canvas.width = 800;
        this.scaling = 800 / this.offsetWidth;
        this.$canvas.height = this.offsetHeight / this.offsetWidth * 800;
        this.$canvas.addEventListener('mousedown', this.onMouseDown.bind(this), false);
        this.$canvas.addEventListener('mousemove', this.onMouseMove.bind(this), false);
        this.$canvas.addEventListener('mouseup', this.onMouseUp.bind(this), false);
        this.$ctx.strokeStyle = "rgba(50, 255, 50, 0.5)";
        this.$ctx.lineWidth = 5;
        this.$ctx.translate(0.5, 0.5);
    },

    getPosition: function (ev) {
        this.rect = this.$canvas.getBoundingClientRect();
        let pos = [ev.layerX*this.scaling, ev.layerY*this.scaling];
        console.log(this.rect);
        console.log(pos);
        //console.log([ev.clientX - this.rect.left, ev.clientY - this.rect.top]);
        return pos;

    },

    onMouseDown: function (ev) {
        console.log(ev);
        this.drawing = true;
        this.position = this.getPosition(ev);
        this.shape = [this.position];
        //this.$ctx.beginPath();
        //alert('Mouse is down!');
    },

    onMouseMove: function (ev) {
        if (!this.drawing) {
            return;
        }
        let x = ev.clientX;
        let y = ev.clientY;
        new_position = this.getPosition(ev);
        this.$ctx.moveTo(this.position[0], this.position[1]);
        this.$ctx.lineTo(new_position[0], new_position[1]);
        this.$ctx.stroke();
        this.position = new_position;
    },

    onMouseUp: function (ev) {
        if (!this.drawing) {
            return;
        }
        this.drawing = false;
        new_position = this.getPosition(ev);
        this.$ctx.moveTo(this.position[0], this.position[1]);
        //this.$ctx.beginPath();
        this.$ctx.lineTo(new_position[0], new_position[1]);

        //this.$ctx.closePath();
        this.$ctx.stroke();
        console.log(this.position);
        this.position = null;
        this.save();
        console.log('Mouse is up!');
        console.log(this.$ctx.strokeStyle);

        //alert('Mouse is up!');
    },

    render: function () {
        if (this.model.get('annotation') !== null) {
            let img = new Image();
            let that = this;
            img.onload = function () {
                that.$ctx.drawImage(img, 0, 0, that.$canvas.width, that.$canvas.height);
                //that.save();
            }
            img.src = 'data:image/png;base64,' + this.model.get('annotation');
            console.log('Annotation found !');
        } else {
            console.log('No annotation found :(');
        }

        this.$ctx.strokeStyle = '#000000';
        this.$ctx.moveTo(0, 0);
        this.$ctx.lineTo(20, 20);
        this.$ctx.stroke();

        //this.$ctx.fillStyle = '#00ff00';
        //this.$ctx.fillRect(0, 0, this.$canvas.width, this.$canvas.height);
    },

    save: function () {
        this.model.save({"annotation": this.$canvas.toDataURL()});
        //console.log(this.$canvas.toDataURL());
        console.log('Saving stuff, eh?');
    }
});

var Annotation = Backbone.Model.extend({
    urlRoot: base_url + "/api/annotation"
});

var Annotations = Backbone.Collection.extend({
    model: Annotation,
    url: base_url + "/api/annotations"
})
