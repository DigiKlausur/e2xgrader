import { Cell } from '@jupyterlab/cells';

/**
 * Represents a mapping of cell types to their corresponding labels.
 */
const labels: { [key: string]: string } = {
  multiplechoice: 'Multiple Choice Answer',
  singlechoice: 'Single Choice Answer',
  diagram: 'Diagram Answer'
};

/**
 * Adds a label to a cell.
 * @param cell - The cell to add the label to.
 * @param label - The label to add to the cell.
 */
export function addCellLabel(cell: Cell, label: string | undefined): void {
  if (!label || !labels[label]) {
    return;
  }
  const node = cell.node;
  // Find the cell header
  const header = node.querySelector('.jp-Cell-header') as HTMLElement;
  // If it has does not have an element with class e2xgrader-cell-label, add it
  if (!header.querySelector('.e2xgrader-cell-label')) {
    const labelElement = document.createElement('div');
    labelElement.classList.add('e2xgrader-cell-label');
    labelElement.textContent = labels[label];
    header.appendChild(labelElement);
  } else {
    // Otherwise, update the text content
    header.querySelector('.e2xgrader-cell-label')!.textContent = labels[label];
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
