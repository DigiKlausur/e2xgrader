let BaseNbgraderUI = Backbone.View.extend({
  animateSaving: function () {
    this.$glyph.removeClass("glyphicon-ok");
    this.$glyph.addClass("glyphicon-refresh");
    this.$glyph.fadeIn(10);
  },

  animateSaved: function () {
    this.$glyph.removeClass("glyphicon-refresh");
    this.$glyph.addClass("glyphicon-ok");
    let that = this;
    setTimeout(function () {
      that.$glyph.fadeOut();
    }, 1000);
    $(document).trigger("finished_saving");
  },
});

let GradeUI = BaseNbgraderUI.extend({
  events: {
    "change .score": "save",
    "change .extra-credit": "save",
    "click .full-credit": "assignFullCredit",
    "click .no-credit": "assignNoCredit",
    "click .mark-graded": "save",
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
    let score, extra_credit;
    if (this.$score.val() === "") {
      score = null;
    } else {
      let val = this.$score.val();
      let max_score = this.model.get("max_score");
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
      let val = this.$extra_credit.val();
      if (val < 0) {
        this.animateInvalidValue(this.$extra_credit);
        extra_credit = 0;
      } else {
        extra_credit = val;
      }
    }

    this.model.save({ manual_score: score, extra_credit: extra_credit });
    this.render();
  },

  animateInvalidValue: function (elem) {
    elem.animate(
      {
        "background-color": "#FF8888",
        "border-color": "red",
      },
      100,
      undefined,
      function () {
        setTimeout(function () {
          elem.animate(
            {
              "background-color": "white",
              "border-color": "white",
            },
            100
          );
        }, 50);
      }
    );
  },

  assignFullCredit: function () {
    this.model.save({ manual_score: this.model.get("max_score") });
    this.$score.select();
    this.$score.focus();
  },

  assignNoCredit: function () {
    this.model.save({ manual_score: 0, extra_credit: 0 });
    this.$score.select();
    this.$score.focus();
  },
});

let Grade = Backbone.Model.extend({
  urlRoot: base_url + "/api/grade",
});

let Grades = Backbone.Collection.extend({
  model: Grade,
  url: base_url + "/api/grades",
});

let CommentUI = BaseNbgraderUI.extend({
  events: {
    "change .comment": "save",
  },

  initialize: function () {
    this.$glyph = this.$el.find(".comment-saved");
    this.$comment = this.$el.find(".comment");

    this.listenTo(this.model, "change", this.render);
    this.listenTo(this.model, "request", this.animateSaving);
    this.listenTo(this.model, "sync", this.animateSaved);

    let default_msg = "Type any comments here (supports Markdown and MathJax)";
    this.$comment.attr(
      "placeholder",
      this.model.get("auto_comment") || default_msg
    );

    this.render();
    autosize(this.$comment);
  },

  render: function () {
    this.$comment.val(this.model.get("manual_comment"));
  },

  save: function () {
    this.model.save({ manual_comment: this.$comment.val() });
  },
});

let Comment = Backbone.Model.extend({
  urlRoot: base_url + "/api/comment",
});

let Comments = Backbone.Collection.extend({
  model: Comment,
  url: base_url + "/api/comments",
});

let AnnotationUI = Backbone.View.extend({
  initialize: function () {
    if (this.$el.length == 0) {
      console.log(
        "Failed to create AnnotationUI. Cell is not present in the notebook"
      );
      return;
    }
    this.$switch = this.$el.find('input[name="annotate"]');
    this.$switch.prop("checked", "checked");

    this.$canvas = this.$el.find(".annotationarea").get(0);
    this.$ctx = this.$canvas.getContext("2d");

    this.$controls = this.$el.find(".paint-controls");

    let that = this;

    this.pencil_cursor = e2x_base_url + "/static/css/pencil-solid.svg";
    this.eraser_cursor = e2x_base_url + "/static/css/eraser-solid.svg";

    $(this.$canvas).css("cursor", "url(" + this.pencil_cursor + ") 0 16, none");

    this.$switch.change(() => {
      if (that.$switch.prop("checked")) {
        that.$canvas.style.pointerEvents = "auto";
        that.$controls.show();
      } else {
        that.$canvas.style.pointerEvents = "none";
        that.$controls.hide();
      }
    });

    this.initializeControls();
    this.initializePaint();
    this.render();
  },

  initializeControls: function () {
    let that = this;

    this.$color = this.$el.find(".color input").get(0);

    $(this.$el.find(".clear").get(0)).click(function () {
      if (confirm("Do you want to delete all annotations?")) {
        that.$ctx.clearRect(0, 0, that.$canvas.width, that.$canvas.height);
        that.save();
      }
    });

    this.$el.find("input[type=radio][name=brush]").change(function () {
      if (this.value == "pencil") {
        that.$ctx.globalCompositeOperation = "source-over";
        $(that.$canvas).css(
          "cursor",
          "url(" + that.pencil_cursor + ") 0 16, none"
        );
      } else if (this.value == "eraser") {
        that.$ctx.globalCompositeOperation = "destination-out";
        $(that.$canvas).css(
          "cursor",
          "url(" + that.eraser_cursor + ") 0 32, none"
        );
      }
    });

    this.$el.find("input[type=radio][name=line-width]").change(function () {
      that.$ctx.lineWidth = this.value / 2;
    });
  },

  initializePaint: function () {
    let that = this;
    this.drawing = false;
    this.edit_mode = true;
    this.position = null;
    this.shape = [];
    this.rect = this.$canvas.getBoundingClientRect();
    this.offsetHeight = this.$canvas.offsetHeight;
    this.offsetWidth = this.$canvas.offsetWidth;
    this.$canvas.width = 800;
    this.scaling = 800 / this.offsetWidth;
    this.$canvas.height = (this.offsetHeight / this.offsetWidth) * 800;
    this.$canvas.addEventListener(
      "mousedown",
      this.onMouseDown.bind(this),
      false
    );
    this.$canvas.addEventListener(
      "mousemove",
      this.onMouseMove.bind(this),
      false
    );
    this.$canvas.addEventListener("mouseup", this.onMouseUp.bind(this), false);
    // Add touch support
    this.$canvas.addEventListener(
      "touchstart",
      function (ev) {
        ev.preventDefault();
        let touch = ev.changedTouches[0];
        let mouseEvent = new MouseEvent("mousedown", {
          clientX: touch.clientX,
          clientY: touch.clientY,
        });
        that.$canvas.dispatchEvent(mouseEvent);
      },
      false
    );
    this.$canvas.addEventListener(
      "touchmove",
      function (ev) {
        ev.preventDefault();
        let touch = ev.changedTouches[0];
        let mouseEvent = new MouseEvent("mousemove", {
          clientX: touch.clientX,
          clientY: touch.clientY,
        });
        that.$canvas.dispatchEvent(mouseEvent);
      },
      false
    );
    this.$canvas.addEventListener(
      "touchend",
      function (ev) {
        ev.preventDefault();
        let touch = ev.changedTouches[0];
        let mouseEvent = new MouseEvent("mouseup", {
          clientX: touch.clientX,
          clientY: touch.clientY,
        });
        that.$canvas.dispatchEvent(mouseEvent);
      },
      false
    );

    this.$ctx.lineWidth = 2.5;
    this.$ctx.translate(0.5, 0.5);
    this.$ctx.imageSmoothingEnabled = false;
    this.$ctx.lineJoin = "round";
    this.$ctx.lineCap = "round";
  },

  getPosition: function (ev) {
    this.rect = this.$canvas.getBoundingClientRect();
    return [
      (ev.clientX - this.rect.left) * this.scaling,
      (ev.clientY - this.rect.top) * this.scaling,
    ];
  },

  onMouseDown: function (ev) {
    this.drawing = true;
    this.position = this.getPosition(ev);
    this.shape = [this.position];
    this.$ctx.beginPath();
    this.$ctx.strokeStyle = this.$color.value;
    this.$ctx.fillStyle = this.$color.value;
  },

  onMouseMove: function (ev) {
    if (!this.drawing) {
      return;
    }
    let new_position = this.getPosition(ev);
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
    let new_position = this.getPosition(ev);
    this.$ctx.moveTo(this.position[0], this.position[1]);
    this.$ctx.lineTo(new_position[0], new_position[1]);
    this.$ctx.stroke();
    this.position = null;
    this.save();
  },

  render: function () {
    if (this.model.get("annotation") !== null) {
      let img = new Image();
      let that = this;
      img.onload = function () {
        that.$ctx.drawImage(img, 0, 0, that.$canvas.width, that.$canvas.height);
      };
      img.src = "data:image/png;base64," + this.model.get("annotation");
    }
  },

  save: function () {
    this.model.save({ annotation: this.$canvas.toDataURL() });
  },
});

let Annotation = Backbone.Model.extend({
  urlRoot: base_url + "/api/annotation",
});

let Annotations = Backbone.Collection.extend({
  model: Annotation,
  url: base_url + "/api/annotations",
});
