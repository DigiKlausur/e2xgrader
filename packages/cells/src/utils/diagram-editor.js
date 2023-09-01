import { urlJoin, requests } from "@e2xgrader/api";
import Jupyter from "base/js/namespace";

let baseOptionsLoaded = false;
let baseOptions = {};

async function fetchBaseOptions() {
  if (!baseOptionsLoaded) {
    try {
      baseOptions = await requests.get(
        urlJoin(Jupyter.notebook.base_url, "e2x", "diagrams", "api")
      );
      baseOptionsLoaded = true;
    } catch (error) {
      console.error("Error fetching DiagramEditor base options:", error);
      baseOptionsLoaded = true;
    }
  }
}

class DiagramEditor {
  constructor(config, ui, done, initialized, urlParams, cell, options = {}) {
    const mergedOptions = { ...baseOptions, ...options };
    this.config = config || this.config;
    this.ui = ui || this.ui;
    this.done = done || function () {};
    this.initialized = initialized || function () {};
    this.urlParams = urlParams;
    this.cell = cell;
    this.handleMessageEvent = this.handleMessageEvent.bind(this);
    this.frame = null;
    this.startElement = null;
    this.format = "xml";
    this.xml = null;
    this.drawDomain = mergedOptions.drawDomain || "https://embed.diagrams.net/";
    this.origin = mergedOptions.drawOrigin || "https://embed.diagrams.net/";
    this.frameStyle =
      "position:absolute;bottom:0;border:0;width:100%;height:100%;";
    this.libs = mergedOptions.libs || [];
  }

  handleMessageEvent(evt) {
    const expectedOrigin = new URL(this.origin);
    const actualOrigin = new URL(evt.origin);
    if (actualOrigin.href !== expectedOrigin.href) {
      console.log(
        `Message should come from ${expectedOrigin.href} but came from ${actualOrigin.href}`
      );
    }
    if (
      this.frame != null &&
      evt.source == this.frame.contentWindow &&
      evt.data.length > 0
    ) {
      try {
        const msg = JSON.parse(evt.data);

        if (msg != null) {
          this.handleMessage(msg);
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  static editElement(cell, elt, config, ui, done, urlParams, options = {}) {
    if (!elt.diagramEditorStarting) {
      elt.diagramEditorStarting = true;

      return new DiagramEditor(
        config,
        ui,
        done,
        function () {
          delete elt.diagramEditorStarting;
        },
        urlParams,
        cell,
        options
      ).editElement(elt);
    }
  }

  static async editDiagram(
    cell,
    elt,
    config,
    ui,
    done,
    urlParams,
    options = {}
  ) {
    fetchBaseOptions().then(() => {
      return this.editElement(cell, elt, config, ui, done, urlParams, options);
    });
  }

  config = null;
  ui = "min";
  xml = null;
  format = "xml";
  libraries = true;
  frameStyle = "position:absolute;bottom:0;border:0;width:100%;height:100%;";

  editElement(elem) {
    const src = this.getElementData(elem);
    this.startElement = elem;
    let fmt = this.format;

    if (src.substring(0, 15) === "data:image/png;") {
      fmt = "xmlpng";
    } else if (
      src.substring(0, 19) === "data:image/svg+xml;" ||
      elem.nodeName.toLowerCase() == "svg"
    ) {
      fmt = "xmlsvg";
    }

    this.startEditing(src, fmt);

    return this;
  }

  getElementData(elem) {
    const name = elem.nodeName.toLowerCase();

    let attribute = "";
    if (name == "svg") {
      attribute = "content";
    } else if (name == "img") {
      attribute = "src";
    } else {
      attribute = "data";
    }

    return elem.getAttribute(attribute);
  }

  setElementData(elem, data) {
    const name = elem.nodeName.toLowerCase();

    if (name == "svg") {
      elem.outerHTML = atob(data.substring(data.indexOf(",") + 1));
    } else {
      elem.setAttribute(name == "img" ? "src" : "data", data);
    }

    return elem;
  }

  startEditing(data, format, title) {
    if (this.frame == null) {
      window.addEventListener("message", this.handleMessageEvent);
      this.format = format || this.format;
      this.title = title || this.title;
      this.data = data;

      this.frame = this.createFrame(this.getFrameUrl(), this.getFrameStyle());
      document.body.appendChild(this.frame);
      this.setWaiting(true);
    }
  }

  setWaiting(waiting) {
    if (this.startElement != null) {
      let elt = this.startElement;
      const name = elt.nodeName.toLowerCase();

      if (name == "svg" || name == "object") {
        elt = elt.parentNode;
      }

      if (elt != null) {
        if (waiting) {
          this.frame.style.pointerEvents = "none";
          this.previousCursor = elt.style.cursor;
          elt.style.cursor = "wait";
        } else {
          elt.style.cursor = this.previousCursor;
          this.frame.style.pointerEvents = "";
        }
      }
    }
  }

  setActive(active) {
    if (active) {
      this.previousOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = this.previousOverflow;
    }
  }

  stopEditing() {
    if (this.frame != null) {
      window.removeEventListener("message", this.handleMessageEvent);
      document.body.removeChild(this.frame);
      this.setActive(false);
      this.frame = null;
    }
  }

  postMessage(msg) {
    if (this.frame != null) {
      this.frame.contentWindow.postMessage(
        JSON.stringify(msg),
        "https://embed.diagrams.net"
      );
    }
  }

  getData() {
    return this.data;
  }

  getTitle() {
    return this.title;
  }

  getFrameStyle() {
    const header = document.getElementById("header");
    return (
      this.frameStyle +
      ";left:" +
      document.body.scrollLeft +
      "px;top:" +
      document.body.scrollTop +
      header.offsetHeight +
      "px;"
    );
  }

  getFrameUrl() {
    let url = this.drawDomain + "?proto=json&spin=1";

    if (this.ui != null) {
      url += "&ui=" + this.ui;
    }

    if (this.libraries != null) {
      url += "&libraries=1";
    }

    if (this.config != null) {
      url += "&configure=1";
    }

    if (this.libs.length > 0) {
      url += "&libs=" + this.libs.join(";");
    }

    if (this.urlParams != null) {
      url += "&" + this.urlParams.join("&");
    }

    console.log("The url", url);

    return url;
  }

  createFrame(url, style) {
    const frame = document.createElement("iframe");
    frame.setAttribute("frameborder", "0");
    frame.setAttribute("style", style);
    frame.setAttribute("src", url);

    return frame;
  }

  setStatus(messageKey, modified) {
    this.postMessage({
      action: "status",
      messageKey: messageKey,
      modified: modified,
    });
  }

  handleMessage(msg) {
    if (msg.event == "configure") {
      this.configureEditor();
    } else if (msg.event == "init") {
      this.initializeEditor();
    } else if (msg.event == "autosave") {
      this.save(msg.xml, true, this.startElement);
    } else if (msg.event == "export") {
      this.cell.model.setAttachment("diagram.png", msg.data);
      this.setElementData(this.startElement, msg.data);
      this.stopEditing();
      this.xml = null;
    } else if (msg.event == "save") {
      this.save(msg.xml, false, this.startElement);
      this.xml = msg.xml;

      if (msg.exit) {
        msg.event = "exit";
      } else {
        this.setStatus("allChangesSaved", false);
      }
    }

    if (msg.event == "exit") {
      this.handleExitMessage(msg);
    }
  }

  handleExitMessage(msg) {
    if (this.format != "xml") {
      if (this.xml != null) {
        this.postMessage({
          action: "export",
          format: this.format,
          xml: this.xml,
          spinKey: "export",
        });
      } else {
        this.stopEditing(msg);
      }
    } else {
      if (msg.modified == null || msg.modified) {
        this.save(msg.xml, false, this.startElement);
      }
      this.stopEditing(msg);
    }
  }

  configureEditor() {
    this.postMessage({ action: "configure", config: this.config });
  }

  initializeEditor() {
    this.postMessage({
      action: "load",
      autosave: 1,
      saveAndExit: "1",
      modified: "unsavedChanges",
      xml: this.getData(),
      title: this.getTitle(),
    });
    this.setWaiting(false);
    this.setActive(true);
    this.initialized();
  }

  save(data, draft, elt) {
    this.done(data, draft, elt);
  }
}

export default DiagramEditor;
