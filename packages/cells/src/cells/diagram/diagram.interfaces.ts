import { IE2xCell } from '../base/base.interfaces';

export type Base64ImageString = `data:${string};base64,${string}`;

export interface IDiagramCell extends IE2xCell {
  updateDiagramAttachment: (attachment: Base64ImageString) => void;
}
