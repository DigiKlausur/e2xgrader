define([
    'jquery',
    './extended_cell',
    './diagram-editor',
    './attachment',
], function(
    $,
    extended_cell,
    diagram_editor,
    attachment
) {

    'use strict';

    let ExtendedCell = extended_cell.ExtendedCell;
    let DiagramEditor = diagram_editor.DiagramEditor;

    class DiagramCell extends ExtendedCell {

        constructor(cell) {
            super(cell, 'diagram');
            this.model = new attachment.DiagramCellModel(cell);
            this.initialize();
        }

        initialize() {
            // Check if we already have an attachment, if not create it
            this.model.load();
            if (!this.model.hasAttachment('diagram.png')) {
                this.model.setAttachment('diagram.png', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAYAAABxLb1rAAAABHNCSVQICAgIfAhkiAAAAylJREFUeJzt1DEBACAMwDDAv+chY0cTBb16Z2YOQNDbDgDYYoBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZH97eBdx+cY1yAAAAAElFTkSuQmCC');
            }
        }

        render() {
            let that = this;

            let attachment_string = '![diagram](attachment:diagram.png)';
            let attachment_comment = '<!-- Display the diagram attachment -->';
            if (this.cell.get_text().indexOf(attachment_string) == -1) {
                this.cell.set_text([
                    this.cell.get_text(),
                    attachment_comment,
                    attachment_string
                ].join('\n'));
            }

            this.cell.render_force();

            let html = $(this.cell.element).find('.rendered_html');



            let img = html.find('img');
            img.addClass('diagram-img');

            // Remove old button if there is any
            $(html).find('.btn-diagram').remove();
            let button = $('<button/>').append('Edit Diagram').addClass('btn-e2x');
            button.click(() => DiagramEditor.editElement(that, img[0]));

            html.append(img);
            html.append(button);
            this.add_edit_button();
        }

    }

    return {
        DiagramCell: DiagramCell,
    };

});