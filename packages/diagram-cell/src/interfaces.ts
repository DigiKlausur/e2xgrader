import { IE2xCell } from '@e2xgrader/cell-core';

export type Base64ImageString = `data:${string};base64,${string}`;

export interface IDiagramCell extends IE2xCell {
  updateDiagramAttachment: (attachment: Base64ImageString) => void;
}

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
