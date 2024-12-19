import { Token } from '@lumino/coreutils';
import { ISignal } from '@lumino/signaling';
import { IE2xCell } from './e2x_cell';

export const ICellRegistry = new Token<ICellRegistry>(
  '@e2xgrader/cell-registry:ICellRegistry'
);

export interface ICellRegistry {
  registerCellType(
    type: string,
    label: string,
    cellClass: new (...args: any[]) => IE2xCell
  ): void;
  getCellClass(type: string): new (...args: any[]) => IE2xCell | undefined;
  cellRegistered: ISignal<
    this,
    { type: string; cellClass: new (...args: any[]) => IE2xCell }
  >;
  getCellTypes(): string[];
  getCellLabel(type: string): string;
}
