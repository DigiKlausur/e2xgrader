import { MarkdownCell, Cell } from '@jupyterlab/cells';
import { E2xGraderMetadata } from './e2x_cell';

export namespace E2xGraderUtils {
  /**
   * Retrieves the e2xgrader metadata from a Markdown cell.
   * @param cell - The Markdown cell to retrieve the metadata from.
   * @returns The e2xgrader metadata object.
   */
  export function getE2xGraderMetadata(
    cell: MarkdownCell
  ): E2xGraderMetadata.IE2xGraderMetadata {
    return (
      cell.model?.getMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY) || {}
    );
  }

  /**
   * Deletes the e2xgrader metadata from a cell.
   * @param cell - The cell to delete the metadata from.
   */
  export function deleteE2xGraderMetadata(cell: Cell): void {
    cell.model?.deleteMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY);
  }

  /**
   * Checks if a given Markdown cell is an e2xgrader cell.
   * @param cell - The Markdown cell to check.
   * @returns `true` if the cell is an e2xgrader cell, `false` otherwise.
   */
  export function isE2xGraderCell(cell: Cell): boolean {
    if (cell.model?.type !== 'markdown') {
      return false;
    }
    return getE2xGraderMetadata(cell as MarkdownCell).type !== undefined;
  }

  /**
   * Retrieves the e2xgrader cell type from the given Markdown cell.
   * @param cell The Markdown cell to retrieve the cell type from.
   * @returns The E2xGrader cell type, or undefined if not found.
   */
  export function getE2xGraderCellType(cell: MarkdownCell): string | undefined {
    return getE2xGraderMetadata(cell).type;
  }

  /**
   * Retrieves the value of a specific field from the e2xgrader metadata of a Markdown cell.
   * If the cell is not an e2xgrader cell or the field does not exist, it returns the defaultValue.
   *
   * @param cell - The Markdown cell to retrieve the field value from.
   * @param field - The name of the field to retrieve.
   * @param defaultValue - The default value to return if the field is not found.
   * @returns The value of the specified field from the e2xgrader metadata, or the defaultValue if the field is not found.
   */
  export function getE2xGraderField(
    cell: MarkdownCell,
    field: string,
    defaultValue: any = {}
  ): any {
    if (!isE2xGraderCell(cell)) {
      return defaultValue;
    }
    const metadata = getE2xGraderMetadata(cell);
    return metadata[field] || defaultValue;
  }

  /**
   * Sets the value of a specific field in the e2xgrader metadata of a Markdown cell.
   *
   * @param cell - The Markdown cell to update.
   * @param field - The name of the field to set.
   * @param value - The value to set for the field.
   */
  export function setE2xGraderField(
    cell: MarkdownCell,
    field: string,
    value: any
  ): void {
    const metadata = getE2xGraderMetadata(cell);
    metadata[field] = value;
    cell.model?.setMetadata(E2xGraderMetadata.E2XGRADER_METADATA_KEY, metadata);
  }

  /**
   * Checks if the E2x grader cell type has changed based on the given change object.
   * @param change - The change object to check.
   * @returns A boolean indicating whether the E2xGrader cell type has changed.
   */
  export function hasE2xGraderCellTypeChanged(change: any): boolean {
    if (change.key !== 'extended_cell') {
      return false;
    }

    if (change.type === 'remove') {
      return true;
    }

    // check if the new value has a key 'type'
    if (!change.newValue?.type) {
      return false;
    }

    // check if there is an old value and if it has a key 'type' and if it is different from the new value
    if (
      change.oldValue?.type &&
      change.oldValue.type === change.newValue.type
    ) {
      return false;
    }

    return true;
  }
}
