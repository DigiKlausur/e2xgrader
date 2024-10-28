import {
  IDiagramCell,
  IDiagramEditorOptions,
  InitializedCallback,
  IDiagramMessage
} from './interfaces';

export class DiagramEditor {
  cell: IDiagramCell;
  initialized: InitializedCallback;
  options: IDiagramEditorOptions;
  frame: HTMLIFrameElement | null;
  startElement: any;
  format: string;
  xml: any;
  frameStyle: string;
  data: any;
  previousCursor: any;
  previousOverflow: any;

  constructor(
    cell: IDiagramCell,
    initialized: InitializedCallback,
    options: IDiagramEditorOptions
  ) {
    this.initialized = initialized || function () {};
    this.cell = cell;
    this.frame = null;
    this.startElement = null;
    this.format = 'xml';
    this.xml = null;
    this.options = options;
    this.frameStyle =
      'position:absolute;bottom:0;border:0;width:100%;height:100%;';
    // We need to bind handleMessageEvent to this so that it can access the class properties
    this.handleMessageEvent = this.handleMessageEvent.bind(this);
  }

  handleMessageEvent(evt: MessageEvent) {
    if (
      this.frame &&
      evt.source === this.frame.contentWindow &&
      evt.data.length > 0
    ) {
      try {
        const msg = JSON.parse(evt.data);

        if (msg !== null) {
          this.handleMessage(msg);
        }
      } catch (e) {
        console.error(e);
      }
    }
  }

  editElement(elem: any) {
    const src = this.getElementData(elem);
    this.startElement = elem;
    let fmt = this.format;

    if (src.substring(0, 15) === 'data:image/png;') {
      fmt = 'xmlpng';
    } else if (
      src.substring(0, 19) === 'data:image/svg+xml;' ||
      elem.nodeName.toLowerCase() === 'svg'
    ) {
      fmt = 'xmlsvg';
    }

    this.startEditing(src, fmt, null);

    return this;
  }

  getElementData(elem: any) {
    const name = elem.nodeName.toLowerCase();

    let attribute = '';
    if (name === 'svg') {
      attribute = 'content';
    } else if (name === 'img') {
      attribute = 'src';
    } else {
      attribute = 'data';
    }

    return elem.getAttribute(attribute);
  }

  setElementData(elem: any, data: any) {
    const name = elem.nodeName.toLowerCase();

    if (name === 'svg') {
      elem.outerHTML = atob(data.substring(data.indexOf(',') + 1));
    } else {
      elem.setAttribute(name === 'img' ? 'src' : 'data', data);
    }

    return elem;
  }

  startEditing(data: any, format: any, title: any) {
    if (this.frame === null || this.frame === undefined) {
      window.addEventListener('message', this.handleMessageEvent);
      this.format = format || this.format;
      this.data = data;

      this.frame = this.createFrame(this.getFrameUrl(), this.getFrameStyle());
      document.body.appendChild(this.frame);
      this.setWaiting(true);
    }
  }

  setWaiting(waiting: any) {
    if (this.startElement && this.frame) {
      let elt = this.startElement;
      const name = elt.nodeName.toLowerCase();

      if (name === 'svg' || name === 'object') {
        elt = elt.parentNode;
      }

      if (elt) {
        if (waiting) {
          this.frame.style.pointerEvents = 'none';
          this.previousCursor = elt.style.cursor;
          elt.style.cursor = 'wait';
        } else {
          elt.style.cursor = this.previousCursor;
          this.frame.style.pointerEvents = '';
        }
      }
    }
  }

  activate() {
    this.previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
  }

  deactivate() {
    document.body.style.overflow = this.previousOverflow;
  }

  stopEditing() {
    if (this.frame !== null) {
      window.removeEventListener('message', this.handleMessageEvent);
      document.body.removeChild(this.frame);
      this.deactivate();
      this.frame = null;
    }
  }

  postMessage(msg: any) {
    if (this.frame?.contentWindow) {
      this.frame.contentWindow.postMessage(
        JSON.stringify(msg),
        this.options.drawOrigin
      );
    }
  }

  getData() {
    return this.data;
  }

  getFrameStyle() {
    const header = document.getElementById('header');
    const headerOffsetHeight = header ? header.offsetHeight : 0;
    return (
      this.frameStyle +
      ';left:' +
      document.body.scrollLeft +
      'px;top:' +
      document.body.scrollTop +
      headerOffsetHeight +
      'px;'
    );
  }

  getFrameUrl() {
    const url = new URL(this.options.drawDomain);
    url.searchParams.append('proto', 'json');
    url.searchParams.append('spin', '1');

    if (this.options.libs && this.options.libs.length > 0) {
      url.searchParams.append('libs', this.options.libs.join(';'));
    }

    return url.href;
  }

  createFrame(url: string, style: string) {
    const frame = document.createElement('iframe');
    frame.setAttribute('frameborder', '0');
    frame.setAttribute('style', style);
    frame.setAttribute('src', url);

    return frame;
  }

  setStatus(messageKey: string, modified: boolean) {
    this.postMessage({
      action: 'status',
      messageKey: messageKey,
      modified: modified
    });
  }

  handleMessage(msg: IDiagramMessage) {
    if (msg.event === 'configure') {
      this.postMessage({ action: 'configure' });
    } else if (msg.event === 'init') {
      this.initializeEditor();
    } else if (msg.event === 'export') {
      this.cell.updateDiagramAttachment(msg.data);
      this.setElementData(this.startElement, msg.data);
      this.stopEditing();
      this.xml = null;
    } else if (msg.event === 'save') {
      this.xml = msg.xml;
      if (msg.exit) {
        msg.event = 'exit';
      } else {
        this.setStatus('allChangesSaved', false);
      }
    }

    if (msg.event === 'exit') {
      this.handleExitMessage();
    }
  }

  handleExitMessage() {
    if (this.format !== 'xml') {
      if (this.xml !== null) {
        this.postMessage({
          action: 'export',
          format: this.format,
          xml: this.xml,
          spinKey: 'export'
        });
      } else {
        this.stopEditing();
      }
    } else {
      this.stopEditing();
    }
  }

  initializeEditor() {
    this.postMessage({
      action: 'load',
      autosave: 1,
      saveAndExit: '1',
      modified: 'unsavedChanges',
      xml: this.getData()
    });
    this.setWaiting(false);
    this.activate();
    this.initialized();
  }
}

export function startDiagramEditor(cell: IDiagramCell, elt: any) {
  console.log(cell.settings);
  const options = {
    drawDomain: cell.settings.get('drawDomain').composite as string,
    drawOrigin: cell.settings.get('drawOrigin').composite as string,
    libs: cell.settings.get('drawLibs').composite as string[]
  };
  const loading = document.createElement('div');
  loading.className = 'e2x_spinner_container';
  const spinner = document.createElement('div');
  spinner.classList.add('jp-SpinnerContent');
  spinner.classList.add('e2x_spinner');
  loading.appendChild(spinner);
  document.body.appendChild(loading);

  return new DiagramEditor(
    cell,
    () => {
      loading.remove();
    },
    options
  ).editElement(elt);
}
