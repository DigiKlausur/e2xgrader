import { Cell, MarkdownCell } from '@jupyterlab/cells';
import {
  RenderUtils,
  NbgraderCellType,
  NbgraderCellTypes,
  NbgraderMetadata,
  E2xGraderMetadata,
  ICellRegistry,
  GradingCellModel
} from '@e2xgrader/cell-core';

export function getAvailableCellTypes(
  cell: Cell,
  cellRegistry: ICellRegistry
): string[][] {
  const available_types = [['', '-']];
  if (cell.model?.type === 'markdown') {
    NbgraderCellTypes.NBGRADER_MARKDOWN_CELL_TYPES.forEach(cellType => {
      available_types.push([
        cellType,
        NbgraderCellTypes.cellTypeLabels[cellType]
      ]);
    });
    cellRegistry.getCellTypes().forEach(cellType => {
      available_types.push([cellType, cellRegistry.getCellLabel(cellType)]);
    });
  } else {
    NbgraderCellTypes.NBGRADER_CODE_CELL_TYPES.forEach(cellType => {
      available_types.push([
        cellType,
        NbgraderCellTypes.cellTypeLabels[cellType]
      ]);
    });
  }
  return available_types;
}

export class GradingCell {
  private readonly _cell: Cell;
  private readonly _gradingCellModel: GradingCellModel;

  constructor(cell: Cell) {
    this._cell = cell;
    this._gradingCellModel = new GradingCellModel(cell.model.sharedModel);
  }

  get model(): GradingCellModel {
    return this._gradingCellModel;
  }

  isNbgraderCellType(value: string): boolean {
    return Object.values(NbgraderCellType).includes(value as NbgraderCellType);
  }

  setNbgraderCellType(cellType: NbgraderCellType): void {
    const metadata =
      this.model.nbgraderMetadata || NbgraderMetadata.newNbGraderMetadata();
    Object.assign(metadata, NbgraderCellTypes.cellTypeConfigurations[cellType]);
    if (!metadata.grade) {
      delete metadata.points;
    } else {
      metadata.points = metadata.points ?? 0;
    }
    this.model.setMetadata(NbgraderMetadata.NBGRADER_METADATA_KEY, metadata);
  }

  setGradingCellType(label: string | undefined): void {
    if (!label) {
      this.model.removeE2xgraderMetadata();
      this.model.removeNbgraderMetadata();
      return;
    }
    if (this.isNbgraderCellType(label)) {
      const nbgraderCellType = label as NbgraderCellType;
      this.model.removeE2xgraderMetadata();
      this.setNbgraderCellType(nbgraderCellType);
    } else {
      this.setNbgraderCellType(NbgraderCellType.MANUALLY_GRADED_ANSWER);
      this.model.setMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY, {
        type: label
      });
    }
    if (this._cell.model.type === 'markdown') {
      RenderUtils.forceRender(this._cell as MarkdownCell);
    }
  }
}
