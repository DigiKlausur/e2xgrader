import { ISharedCell, SharedCell } from '@jupyter/ydoc';
import {
  NbgraderMetadata,
  NbgraderCellType,
  NbgraderCellTypes
} from './nbgrader';
import { E2xGraderMetadata } from './e2x_cell';

export class GradingCellModel {
  private readonly _cell: ISharedCell;
  constructor(cell: ISharedCell) {
    this._cell = cell;
  }

  getMetadata(key: string): any {
    return this._cell.getMetadata(key);
  }

  setMetadata(key: string, value: any): void {
    this._cell.setMetadata(key, value);
  }

  setNestedMetadata(key: string, nestedKey: string, value: any): void {
    const metadata = this.getMetadata(key) || {};
    if (value === undefined) {
      delete metadata[nestedKey];
    } else {
      metadata[nestedKey] = value;
    }
    this.setMetadata(key, metadata);
  }

  removeNbgraderMetadata(): void {
    this._cell.deleteMetadata(NbgraderMetadata.NBGRADER_METADATA_KEY);
  }

  removeE2xgraderMetadata(): void {
    this._cell.deleteMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY);
  }

  setNbgraderMetadataKey(nestedKey: string, value: any): void {
    this.setNestedMetadata(
      NbgraderMetadata.NBGRADER_METADATA_KEY,
      nestedKey,
      value
    );
  }

  getE2xgraderMetadataKey(nestedKey: string, default_value: any = {}): any {
    return this.e2xgraderMetadata?.[nestedKey] ?? default_value;
  }

  setE2xgraderMetadataKey(nestedKey: string, value: any): void {
    this.setNestedMetadata(
      E2xGraderMetadata.E2XGRADER_METADATA_KEY,
      nestedKey,
      value
    );
  }

  get nbgraderMetadata(): NbgraderMetadata.INbgraderMetadata | undefined {
    return this.getMetadata(NbgraderMetadata.NBGRADER_METADATA_KEY);
  }

  get e2xgraderMetadata(): E2xGraderMetadata.IE2xGraderMetadata | undefined {
    return this.getMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY);
  }

  get isNbgraderCell(): boolean {
    return !!this.nbgraderMetadata;
  }

  get isE2xgraderCell(): boolean {
    return !!this.e2xgraderMetadata;
  }

  get isGrade(): boolean {
    return this.nbgraderMetadata?.grade ?? false;
  }

  set isGrade(value: boolean) {
    this.setNbgraderMetadataKey('grade', value);
  }

  get isSolution(): boolean {
    return this.nbgraderMetadata?.solution ?? false;
  }

  set isSolution(value: boolean) {
    this.setNbgraderMetadataKey('solution', value);
  }

  get isTask(): boolean {
    return this.nbgraderMetadata?.task ?? false;
  }

  set isTask(value: boolean) {
    this.setNbgraderMetadataKey('task', value);
  }

  get isLocked(): boolean {
    return this.nbgraderMetadata?.locked ?? false;
  }

  set isLocked(value: boolean) {
    this.setNbgraderMetadataKey('locked', value);
  }

  get gradeId(): string | undefined {
    return this.nbgraderMetadata?.grade_id;
  }

  set gradeId(value: string | undefined) {
    this.setNbgraderMetadataKey('grade_id', value);
  }

  get points(): number | undefined {
    return this.nbgraderMetadata?.points;
  }

  set points(value: number | undefined) {
    this.setNbgraderMetadataKey('points', value);
  }

  get e2xgraderType(): string | undefined {
    return this.e2xgraderMetadata?.type;
  }

  get gradingCellType(): string | undefined {
    return (
      this.e2xgraderType ??
      NbgraderCellTypes.findMatchingCellType(this.nbgraderMetadata)
    );
  }

  private matchesCellType(cellType: NbgraderCellType): boolean {
    return NbgraderCellTypes.matchesCellType(this.nbgraderMetadata, cellType);
  }

  get isDescription(): boolean {
    return this.matchesCellType(NbgraderCellType.DESCRIPTION);
  }

  get isAutograderTest(): boolean {
    return this.matchesCellType(NbgraderCellType.AUTOGRADER_TEST);
  }

  get isAutograderSolution(): boolean {
    return this.matchesCellType(NbgraderCellType.AUTOGRADED_ANSWER);
  }

  get isManualGradingCell(): boolean {
    return this.matchesCellType(NbgraderCellType.MANUALLY_GRADED_ANSWER);
  }

  toJSON(): SharedCell.Cell {
    return this._cell.toJSON();
  }
}
