export interface IDiagramEditorOptions {
  drawDomain: string;
  drawOrigin: string;
  libs?: string[];
}

export type InitializedCallback = () => void;

type DiagramMessageEvent =
  | 'configure'
  | 'init'
  | 'autosave'
  | 'export'
  | 'save'
  | 'exit';

export interface IDiagramMessage {
  event: DiagramMessageEvent;
  xml: any;
  data: any;
  modified: any;
  exit: any;
}
