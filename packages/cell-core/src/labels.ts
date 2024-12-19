import { Cell } from '@jupyterlab/cells';

export namespace CellLabel {
  export const CELL_LABEL_CLASS = 'e2xgrader-cell-label';
  export const CELL_HEADER_CLASS = 'jp-Cell-header';
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

    const addOrUpdateLabel = (header: HTMLElement) => {
      if (!header.querySelector(`.${CELL_LABEL_CLASS}`)) {
        const labelElement = document.createElement('div');
        labelElement.classList.add(CELL_LABEL_CLASS);
        labelElement.textContent = label;
        header.appendChild(labelElement);
      } else {
        header.querySelector(`.${CELL_LABEL_CLASS}`)!.textContent = label;
      }
    };

    const header = node.querySelector(`.${CELL_HEADER_CLASS}`) as HTMLElement;
    if (header) {
      addOrUpdateLabel(header);
    } else {
      const observer = new MutationObserver((_mutations, obs) => {
        const header = node.querySelector(
          `.${CELL_HEADER_CLASS}`
        ) as HTMLElement;
        if (header) {
          addOrUpdateLabel(header);
          obs.disconnect();
        }
      });

      observer.observe(node, { childList: true, subtree: true });

      // Set a timeout to stop observing after a certain period
      setTimeout(() => {
        observer.disconnect();
      }, 5000); // 5 seconds timeout
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
    const header = node.querySelector(`.${CELL_HEADER_CLASS}`) as HTMLElement;
    if (!header) {
      return;
    }
    const label = header.querySelector(`.${CELL_LABEL_CLASS}`);
    if (label) {
      header.removeChild(label);
    }
  }
}
