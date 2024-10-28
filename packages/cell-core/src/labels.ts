import { Cell } from '@jupyterlab/cells';

export namespace CellLabel {
  /**
   * Adds a label to a cell.
   * @param cell - The cell to add the label to.
   * @param label - The label to add to the cell.
   */
  export function addCellLabel(cell: Cell, label: string | undefined): void {
    if (!label) {
      return;
    }
    const node = cell.node;
    // Find the cell header
    const header = node.querySelector('.jp-Cell-header') as HTMLElement;
    // If it has does not have an element with class e2xgrader-cell-label, add it
    if (!header.querySelector('.e2xgrader-cell-label')) {
      const labelElement = document.createElement('div');
      labelElement.classList.add('e2xgrader-cell-label');
      labelElement.textContent = label;
      header.appendChild(labelElement);
    } else {
      // Otherwise, update the text content
      header.querySelector('.e2xgrader-cell-label')!.textContent = label;
    }
  }

  /**
   * Removes the cell label from a given cell.
   *
   * This function searches for an element with the class `e2xgrader-cell-label`
   * within the header of the specified cell and removes it if found.
   *
   * @param cell - The cell from which the label should be removed.
   */
  export function removeCellLabel(cell: Cell): void {
    const node = cell.node;
    const header = node.querySelector('.jp-Cell-header') as HTMLElement;
    const label = header.querySelector('.e2xgrader-cell-label');
    if (label) {
      header.removeChild(label);
    }
  }
}
