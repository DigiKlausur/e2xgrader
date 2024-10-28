import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { MarkdownCell } from '@jupyterlab/cells';
import { E2xGraderUtils, ICellRegistry } from '@e2xgrader/cell-core';

/**
 * The `CellFactory` class is a singleton responsible for creating e2xgrader cell instances
 * based on the provided cell type. It uses a cell registry and settings to
 * instantiate the appropriate e2xgrader cell class.
 *
 * @remarks
 * This class ensures that only one instance of `CellFactory` exists and provides
 * a static method to initialize it. It also provides a static method to create
 * e2xgrader cells.
 *
 * @example
 * ```typescript
 * // Initialize the CellFactory
 * CellFactory.initialize(cellRegistry, settings);
 *
 * // Create an e2xgrader cell
 * const cell = CellFactory.createCell(markdownCell);
 * ```
 *
 * @public
 */
export class CellFactory {
  private static instance: CellFactory;
  private readonly cellRegistry: ICellRegistry;
  private readonly settings: ISettingRegistry.ISettings;

  private constructor(
    cellRegistry: ICellRegistry,
    settings: ISettingRegistry.ISettings
  ) {
    this.cellRegistry = cellRegistry;
    this.settings = settings;
  }

  /**
   * Initializes the CellFactory singleton instance if it hasn't been created yet.
   *
   * @param cellRegistry - The registry of cell types.
   * @param settings - The settings for the cell factory.
   */
  public static initialize(
    cellRegistry: ICellRegistry,
    settings: ISettingRegistry.ISettings
  ): void {
    if (!CellFactory.instance) {
      CellFactory.instance = new CellFactory(cellRegistry, settings);
    }
  }

  /**
   * Creates a new cell instance based on the provided MarkdownCell.
   *
   * @param cell - The MarkdownCell to be used for creating the new cell instance.
   * @returns A new cell instance if the cell type is recognized, otherwise null.
   * @throws Error if the CellFactory is not initialized.
   */
  public static createCell(cell: MarkdownCell) {
    if (!CellFactory.instance) {
      throw new Error(
        'CellFactory is not initialized. Call initialize() first.'
      );
    }

    const cellType = E2xGraderUtils.getE2xGraderCellType(cell);
    if (!cellType) {
      return null;
    }

    const cellClass = CellFactory.instance.cellRegistry.getCellClass(cellType);
    return cellClass
      ? new cellClass(cell, CellFactory.instance.settings)
      : null;
  }
}
