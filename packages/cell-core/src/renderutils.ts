import { MarkdownCell } from '@jupyterlab/cells';
import { MimeModel } from '@jupyterlab/rendermime';

export namespace RenderUtils {
  /**
   * Retrieves the HTML element containing the rendered markdown content of a MarkdownCell.
   * Waits until the HTML is available or a timeout is reached.
   *
   * @param cell - The MarkdownCell to retrieve the HTML element from.
   * @param interval - The interval in milliseconds to check for the HTML. Default is 100ms.
   * @param timeout - The timeout in milliseconds to stop checking for the HTML. Default is 5000ms.
   * @returns A promise that resolves with the HTML element or rejects if not found within the timeout.
   */
  export async function getHTML(
    cell: MarkdownCell,
    interval: number = 100,
    timeout: number = 5000
  ): Promise<Element> {
    const startTime = Date.now();

    return new Promise((resolve, reject) => {
      const checkHTML = () => {
        const html = cell.node.getElementsByClassName('jp-RenderedMarkdown');
        if (html.length > 0) {
          resolve(html[0]);
        } else if (Date.now() - startTime >= timeout) {
          reject(new Error('HTML not found within the timeout period'));
        } else {
          setTimeout(checkHTML, interval);
        }
      };

      checkHTML();
    });
  }

  /**
   * Forces the rendering of a Markdown cell.
   *
   * @param cell - The Markdown cell to render.
   */
  export function forceRender(cell: MarkdownCell): void {
    const text =
      cell.model?.sharedModel.getSource() || 'Type Markdown and LaTeX: $ a^2 $';
    const readOnly = cell.readOnly;
    cell.readOnly = false;
    cell.rendered = false;
    cell.renderer
      .renderModel(new MimeModel({ data: { 'text/markdown': text } }))
      .then(() => {
        cell.rendered = true;
        cell.readOnly = readOnly;
      });
  }
}
