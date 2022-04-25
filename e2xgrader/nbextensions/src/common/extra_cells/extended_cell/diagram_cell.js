define([
    'jquery',
    './extended_cell',
    './diagram-editor',
    './attachment',
], function (
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
            this.edit_mode = false;
            this.initialize();
        }

        initialize = function () {
            // Check if we already have an attachment, if not create it
            this.model.load();
            if (!this.model.hasAttachment('diagram.png')) {
                this.model.setAttachment('diagram.png', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAUAAAADwCAYAAABxLb1rAAAABHNCSVQICAgIfAhkiAAAAylJREFUeJzt1DEBACAMwDDAv+chY0cTBb16Z2YOQNDbDgDYYoBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZBghkGSCQZYBAlgECWQYIZBkgkGWAQJYBAlkGCGQZIJBlgECWAQJZH97eBdx+cY1yAAAAAElFTkSuQmCC');
            }
        }

        get_edit_button = function () {
            let that = this;
            return $('<button>')
                .attr('type', 'button')
                .addClass('hbrs_unrender')
                .click(function () {
                    that.cell.unrender_force();
                }).append('Edit cell');
        }

        render = function() {
            let that = this;

            this.cell.set_text('![diagram](attachment:diagram.png)');            
            this.cell.render_force();            

            let html = $(this.cell.element).find('.rendered_html');            
            

            
            let img = html.find('img');
            img.addClass('diagram-img');

            // Remove old button if there is any
            $(html).find('.btn-diagram').remove();
            let button = $('<button/>').append('Edit Diagram').addClass('btn-diagram');
            button.click(() => DiagramEditor.editElement(that, img[0]));
            
            html.append(img);
            if (this.edit_mode) {
                html.append(this.get_edit_button());
            }
            html.append(button);
        }

    }

    return {
        DiagramCell: DiagramCell,
    };

});
