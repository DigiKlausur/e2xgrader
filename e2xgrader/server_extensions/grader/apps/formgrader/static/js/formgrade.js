function FormGrader(base_url, submission_id) {
  this.base_url = base_url;
  this.submission_id = submission_id;

  this.loaded = false;
}

FormGrader.prototype.init = function () {
  this.loadGrades();
  this.loadComments();
  this.loadAnnotations();
  this.collapsibleCells();

  // disable link selection on tabs
  $("a:not(.tabbable)").attr("tabindex", "-1");

  this.configureTooltips();
  this.configureScrolling();

  this.keyboard_manager = new KeyboardManager();
  this.keyboard_manager.register({
    handler: _.bind(this.selectNextInput, this),
    keybinding: "tab",
    help: "Move to the next score or comment input",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.selectPrevInput, this),
    keybinding: "shift-tab",
    help: "Move to the previous score or comment input",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.defocusInput, this),
    selector: ".tabbable",
    keybinding: "escape",
    help: "Defocus and save the current score or comment input",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.focusInput, this),
    keybinding: "enter",
    help: "Refocus the most recent score or comment input",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.nextAssignment, this),
    keybinding: "control-.",
    help: "Move to the same score or comment input of the next submission",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.nextIncorrectAssignment, this),
    keybinding: "control-shift-.",
    help: "Move to the same score or comment input of the next submission with failed tests",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.prevAssignment, this),
    keybinding: "control-,",
    help: "Move to the same score or comment input of the previous submission",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.prevIncorrectAssignment, this),
    keybinding: "control-shift-,",
    help: "Move to the same score or comment input of the previous submission with failed tests",
  });
  this.keyboard_manager.register({
    handler: _.bind(this.flag, this),
    keybinding: "control-shift-f",
    help: "Flag the submission",
  });

  this.loaded = true;
};

FormGrader.prototype.collapsibleCells = function () {
  $(".collapsible").each(function (idx, elem) {
    let button = $(elem);
    let body = button.parent().parent().find(".panel-body");

    button.on("click", function () {
      $(body).toggle();
      if ($(body).is(":hidden")) {
        button.text("Show Test Code");
      } else {
        button.text("Hide Test Code");
      }
    });
  });
};

FormGrader.prototype.loadGrades = function () {
  let that = this;

  this.grades = new Grades();
  this.grade_uis = [];
  this.grades.loaded = false;
  this.grades.fetch({
    data: {
      submission_id: this.submission_id,
    },
    success: function () {
      that.grades.each(function (model) {
        let grade_ui = new GradeUI({
          model: model,
          el: $("#" + model.get("name")).parents(".nbgrader_cell"),
        });
        that.grade_uis.push(grade_ui);
      });
      that.grades.loaded = true;
    },
  });
};

FormGrader.prototype.loadComments = function () {
  let that = this;

  this.comments = new Comments();
  this.comment_uis = [];
  this.comments.loaded = false;
  this.comments.fetch({
    data: {
      submission_id: this.submission_id,
    },
    success: function () {
      that.comments.each(function (model) {
        let comment_ui = new CommentUI({
          model: model,
          el: $("#" + model.get("name") + "-comment").parents(".nbgrader_cell"),
        });
        that.comment_uis.push(comment_ui);
      });
      that.comments.loaded = true;
    },
  });
};

FormGrader.prototype.loadAnnotations = function () {
  let that = this;

  this.annotations = new Annotations();
  this.annotation_uis = [];
  this.annotations.loaded = false;
  this.annotations.fetch({
    data: {
      submission_id: this.submission_id,
    },
    success: function () {
      that.annotations.each(function (model) {
        if (model.get("name").includes(task_id)) {
          let annotation_ui = new AnnotationUI({
            model: model,
            el: $("#" + model.get("name") + "-canvas").parents(".cell"),
          });
          that.annotation_uis.push(annotation_ui);
        }
      });
      that.annotations.loaded = true;
    },
  });
};

FormGrader.prototype.navigateTo = function (location) {
  return (
    this.base_url +
    "/submissions/" +
    this.submission_id +
    "/" +
    location +
    "?index=" +
    this.current_index +
    "&task=" +
    task_id
  );
};

FormGrader.prototype.nextAssignment = function () {
  let url = this.navigateTo("next");
  this.save(function () {
    window.location = url;
  });
};

FormGrader.prototype.nextIncorrectAssignment = function () {
  let url = this.navigateTo("next_incorrect");
  this.save(function () {
    window.location = url;
  });
};

FormGrader.prototype.prevAssignment = function () {
  let url = this.navigateTo("prev");
  this.save(function () {
    window.location = url;
  });
};

FormGrader.prototype.prevIncorrectAssignment = function () {
  let url = this.navigateTo("prev_incorrect");
  this.save(function () {
    window.location = url;
  });
};

FormGrader.prototype.save = function (callback) {
  let elem = document.activeElement;
  if (elem.tagName === "INPUT" || elem.tagName === "TEXTAREA") {
    if (callback) {
      $(document).on("finished_saving", callback);
    }
    $(elem).blur();
    $(elem).trigger("change");
  } else {
    callback();
  }
};

FormGrader.prototype.getScrollPosition = function () {
  let target = this.last_selected.parents(".nbgrader_cell");
  if (target.length === 0) {
    return $("body").offset().top;
  } else {
    return target.offset().top - $(window).height() * 0.33 + 60;
  }
};

FormGrader.prototype.getIndex = function (elem) {
  if (elem !== undefined) {
    let elems = $(".tabbable");
    return elems.index(elem);
  } else {
    return parseInt(getParameterByName(index)) || 0;
  }
};

FormGrader.prototype.selectInput = function (index) {
  let elems = $(".tabbable");
  if (index === elems.length) {
    index = 0;
  } else if (index === -1) {
    index = elems.length - 1;
  }
  $(elems[index]).select();
  $(elems[index]).focus();
};

FormGrader.prototype.selectNextInput = function (e) {
  e.preventDefault();
  e.stopPropagation();
  this.selectInput(this.getIndex(this.last_selected) + 1);
};

FormGrader.prototype.selectPrevInput = function (e) {
  e.preventDefault();
  e.stopPropagation();
  this.selectInput(this.getIndex(this.last_selected) - 1);
};

FormGrader.prototype.defocusInput = function (e) {
  $(e.currentTarget).blur();
};

FormGrader.prototype.focusInput = function (e) {
  if (this.last_selected[0] !== document.activeElement) {
    e.preventDefault();
    e.stopPropagation();

    $("body, html").scrollTop(this.getScrollPosition());
    this.last_selected.select();
    this.last_selected.focus();
  }
};

FormGrader.prototype.configureTooltips = function () {
  $("li.previous a").tooltip({ container: "body" });
  $("li.next a").tooltip({ container: "body" });
  $("li.live-notebook a").tooltip({ container: "body" });
};

FormGrader.prototype.setIndexFromUrl = function () {
  let name = "index";

  // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
  name = name.replace(/\[/, "\\[").replace(/\]/, "\\]");
  let regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
  let index =
    results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));

  this.setCurrentIndex(parseInt(index) || 0);
  this.last_selected = $($(".tabbable")[this.current_index]);
};

FormGrader.prototype.setCurrentIndex = function (index) {
  // if an index is not provided, then we compute it based
  // on whatver the most recently selected element was
  if (index === undefined) {
    let target = this.last_selected.parents(".nbgrader_cell").find(".score");
    if (target.length === 0) {
      this.current_index = this.getIndex(this.last_selected);
    } else {
      this.current_index = this.getIndex(target);
    }

    // otherwise we do some value checking and just set the
    // value directly
  } else {
    if (index < 0) {
      this.current_index = 0;
    } else if (index > $(".tabbable").length) {
      this.current_index = $(".tabbable").length;
    } else {
      this.current_index = index;
    }
  }
};

FormGrader.prototype.scrollToLastSelected = function () {
  this.setCurrentIndex();
  history.replaceState(history.state, "", this.navigateTo(""));

  let that = this;
  $("body, html").stop().animate(
    {
      scrollTop: that.getScrollPosition(),
    },
    500
  );
};

FormGrader.prototype.configureScrolling = function () {
  let that = this;
  $(".tabbable").focus(function (event) {
    if (that.last_selected[0] !== event.currentTarget) {
      that.last_selected = $(event.currentTarget);
      that.scrollToLastSelected();
    }
  });

  this.setIndexFromUrl();

  MathJax.loaded = false;
  MathJax.Hub.Startup.signal.Interest(function (message) {
    if (message === "End") {
      that.last_selected.select();
      that.last_selected.focus();
      MathJax.loaded = true;
      that.scrollToLastSelected();
    }
  });
};

FormGrader.prototype.flag = function () {
  $.ajax({
    method: "POST",
    url: base_url + "/api/submitted_notebook/" + submission_id + "/flag",
    headers: { "X-CSRFToken": getCookie("_xsrf") },
    success: function (data, status, xhr) {
      let elem = $("#statusmessage");
      data = JSON.parse(data);
      if (data.flagged) {
        elem.text("Submission flagged");
        elem.css({
          color: "rgba(255, 0, 0, 0.6)",
        });
        elem.show();
      } else {
        elem.text("Submission unflagged");
        elem.css({
          color: "rgba(0, 100, 0, 0.6)",
        });
        elem.show();
      }
      setTimeout(function () {
        elem.fadeOut(500);
      }, 500);
    },
  });
};

let formgrader = new FormGrader(base_url, submission_id);
$(window).on("load", function () {
  formgrader.init();
});
