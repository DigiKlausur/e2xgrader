define(["require"], function (require) {
  "use strict";

  var load_css = function () {
    var link = document.createElement("link");
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = require.toUrl("./treeview.css");
    document.getElementsByTagName("head")[0].appendChild(link);
  };

  var load_ipython_extension = function () {
    load_css();
  };

  return {
    load_ipython_extension: load_ipython_extension,
  };
});
