import { MarkdownCell } from '@jupyterlab/cells';
import {
  E2xGraderUtils,
  RenderUtils,
  ICellRegistry
  //CellLabel
} from '@e2xgrader/cell-core';
import { CellFactory } from './factory';

/**
 * Namespace containing functions to handle cell rendering and metadata changes.
 */
export namespace CellHandlers {
  /**
   * Handles the rendering of a Markdown cell by creating an E2x cell and updating its label.
   *
   * This function performs the following steps:
   * 1. Creates an E2x cell from the given Markdown cell.
   * 2. If the E2x cell is successfully created, it triggers the `onCellRendered` method and adds a label to the cell.
   * 3. If the E2x cell is not created, it removes any existing label from the cell.
   *
   * @param cell - The Markdown cell to be rendered and processed.
   */
  export function handleCellRendering(cell: MarkdownCell) {
    const e2xCell = CellFactory.createCell(cell);
    if (e2xCell) {
      e2xCell.onCellRendered();
      //CellLabel.addCellLabel(cell, E2xGraderUtils.getE2xGraderCellType(cell));
    } else {
      //CellLabel.removeCellLabel(cell);
    }
  }

  /**
   * Listens to metadata changes on a given Markdown cell and triggers actions
   * based on specific metadata changes.
   *
   * @param cell - The MarkdownCell instance to listen for metadata changes.
   *
   * The function connects to the `metadataChanged` signal of the cell's model.
   * When metadata changes, it checks if the e2xgrader cell type has changed
   * using `E2xGraderUtils.hasE2xGraderCellTypeChanged`. If the cell type has
   * changed, it forces a re-render of the cell using `RenderUtils.forceRender`.
   */
  export function listenToMetadataChanges(cell: MarkdownCell) {
    const model = cell.model;
    model.metadataChanged.connect((_: any, args: any) => {
      if (E2xGraderUtils.hasE2xGraderCellTypeChanged(args)) {
        RenderUtils.forceRender(cell);
      }
    });
  }

  /**
   * Attaches a listener to a MarkdownCell that triggers when the cell's rendered state changes.
   *
   * @param cell - The MarkdownCell to attach the listener to.
   */
  export function listenToRenderChanges(cell: MarkdownCell) {
    cell.renderedChanged.connect((_: any, isRendered: boolean) => {
      if (!isRendered) {
        return;
      }
      handleCellRendering(cell);
    });
  }

  /**
   * Registers a listener for new cells being registered in the cell registry.
   * When a new cell is registered, it checks if the cell type matches the type
   * of the provided cell. If it matches, it triggers the cell rendering handler.
   *
   * @param cell - The MarkdownCell instance to be monitored.
   * @param cellRegistry - The registry where cells are registered.
   */
  export function listenToNewCellRegistered(
    cell: MarkdownCell,
    cellRegistry: ICellRegistry
  ) {
    cellRegistry.cellRegistered.connect((_, { type }) => {
      if (type !== E2xGraderUtils.getE2xGraderCellType(cell)) {
        return;
      }
      handleCellRendering(cell);
    });
  }
}
