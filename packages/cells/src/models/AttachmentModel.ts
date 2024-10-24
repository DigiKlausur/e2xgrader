import E2xCell from '../cells/base/BaseCell';

export interface IObserver {
  notify(event: any): void;
}

interface IObservable {
  registerObserver(observer: IObserver): void;
  notifyAll(event: any): void;
}

interface IAttachment {
  id: number;
  name: string;
  type: string;
  data: string;
}

class Observable implements IObservable {
  private observers: any[];

  constructor() {
    this.observers = [];
  }

  registerObserver(observer: IObserver) {
    this.observers.push(observer);
  }

  notifyAll(event: any) {
    this.observers.forEach(observer => observer.notify(event));
  }
}

export default class AttachmentModel extends Observable {
  private ids: { [key: string]: number };
  e2xCell: E2xCell;
  cell: any;
  private typePattern: RegExp;
  private attachments: { [key: string]: { [key: string]: string } };
  private id: number;

  constructor(cell: any) {
    super();
    this.ids = {};
    this.e2xCell = cell;
    this.cell = this.e2xCell.cell;
    this.typePattern = /data:([^;]*)/;
    this.attachments = {};
    this.id = 0;
    this.load();
  }

  load() {
    this.id = 0;
    Object.assign(this.attachments, this.cell.model.sharedModel.attachments);
    Object.keys(this.attachments).forEach(key => {
      this.id += 1;
      this.ids[key] = this.id;
    });
  }

  save() {
    this.cell.model.sharedModel.attachments = this.attachments;
    this.postSaveHook();
  }

  postSaveHook() {
    // Invoked after attachments are saved
  }

  hasAttachment(key: string) {
    return key in this.attachments;
  }

  getAttachment(key: string): IAttachment {
    return {
      id: this.ids[key],
      name: key,
      type: Object.keys(this.attachments[key])[0],
      data: Object.values(this.attachments[key])[0]
    };
  }

  setAttachment(key: string, dataUrl: string) {
    const match = this.typePattern.exec(dataUrl);
    const type = match ? match[1] : '';
    const data = dataUrl.replace('data:' + type + ';base64,', '');
    this.id += 1;
    this.attachments[key] = {};
    this.attachments[key][type] = data;
    this.ids[key] = this.id;
    this.notifyAll({
      type: 'add',
      key: key,
      id: this.ids[key]
    });
    this.save();
  }

  removeAttachment(key: string) {
    const id = this.ids[key];
    delete this.attachments[key];
    delete this.ids[key];
    this.notifyAll({
      type: 'delete',
      key: key,
      id: id
    });
    this.save();
  }

  getAttachments() {
    const attachments: IAttachment[] = [];
    Object.keys(this.attachments).forEach(key => {
      attachments.push(this.getAttachment(key));
    });
    return attachments;
  }
}
