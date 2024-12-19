import { ISignal, Signal } from '@lumino/signaling';
import { IE2xCell, ICellRegistry } from '@e2xgrader/cell-core';

export class CellRegistry implements ICellRegistry {
  private cellClasses: { [key: string]: new (...args: any[]) => IE2xCell } = {};
  private cellLabels: { [key: string]: string } = {};
  private readonly _cellRegistered = new Signal<
    this,
    { type: string; cellClass: new (...args: any[]) => IE2xCell }
  >(this);

  get cellRegistered(): ISignal<
    this,
    { type: string; cellClass: new (...args: any[]) => IE2xCell }
  > {
    return this._cellRegistered;
  }

  registerCellType(
    type: string,
    label: string,
    cellClass: new (...args: any[]) => IE2xCell
  ): void {
    this.cellClasses[type] = cellClass;
    this.cellLabels[type] = label;
    this._cellRegistered.emit({ type, cellClass });
  }

  getCellClass(type: string): new (...args: any[]) => IE2xCell | undefined {
    return this.cellClasses[type];
  }

  getCellTypes(): string[] {
    return Object.keys(this.cellClasses);
  }

  getCellLabel(type: string): string {
    return this.cellLabels[type];
  }
}
