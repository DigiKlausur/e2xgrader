define([
    'jquery',
    'require',
    'base/js/namespace',
    'base/js/events',
    'base/js/markdown',
    'notebook/js/textcell',
    'notebook/js/notebook',
    './extended_cell/extended_cell',
    './extended_cell/choice_cell',
    './extended_cell/attachment_cell',
    './extended_cell/pdf_cell',
    './extended_cell/form_cell',
], function (
    $,
    require,
    Jupyter,
    events,
    markdown,
    textcell,
    notebook,
    extended_cell,
    choice_cell,
    attachment_cell,
    pdf_cell,
    form_cell,
) {

    'use strict';

    let MarkdownCell = textcell.MarkdownCell;
    let TextCell = textcell.TextCell;
    let old_render = MarkdownCell.prototype.render;
    let old_unrender = MarkdownCell.prototype.unrender;
    let old_toJSON = TextCell.prototype.toJSON;
    let old_to_markdown = notebook.Notebook.prototype.to_markdown;
    let edit_mode = false;


    /**
    * Create a new unsafe render function for markdown cells
    * This is needed if we want to embed external content
    * such as PDFs
    */
    MarkdownCell.prototype.unsafe_render = function () {
        this.drag_counter = 0;
        this.inner_cell.removeClass('dropzone');

        var cont = TextCell.prototype.render.apply(this);
        if (cont) {
            var that = this;
            var text = this.get_text();
            if (text === "") { text = this.placeholder; }

            markdown.render(text, {
                with_math: true,
                clean_tables: true,
                sanitize: false,
            }, function (err, html) {
                html = $(html);
                // add anchors to headings
                html.find(":header").addBack(":header").each(function (i, h) {
                    h = $(h);
                    var hash = h.text().replace(/ /g, '-');
                    h.attr('id', hash);
                    h.append(
                        $('<a/>')
                            .addClass('anchor-link')
                            .attr('href', '#' + hash)
                            .text('¶')
                            .on('click',function(){
                                setTimeout(function(){that.unrender(); that.render()}, 100)
                            })
                    );
                });
                // links in markdown cells should open in new tabs
                html.find("a[href]").not('[href^="#"]').attr("target", "_blank");
                // replace attachment:<key> by the corresponding entry
                // in the cell's attachments
                html.find('img[src^="attachment:"]').each(function (i, h) {
                  h = $(h);
                  var key = h.attr('src').replace(/^attachment:/, '');

                  if (that.attachments.hasOwnProperty(key)) {
                    var att = that.attachments[key];
                    var mime = Object.keys(att)[0];
                    h.attr('src', 'data:' + mime + ';base64,' + att[mime]);
                  } else {
                    h.attr('src', '');
                  }
                });
                that.set_rendered(html);
                that.typeset();
                that.events.trigger("rendered.MarkdownCell", {cell: that});
            });
        }
        return cont;
    }

    /**
    * Check whether a cell is an extra cell
    */
    function is_extra_cell(cell) {
        return cell.cell_type == 'markdown' && cell.metadata.hasOwnProperty('extended_cell');
    }

    /**
    * Get the cell type of a cell
    *
    * @return {string} standard cell type or extended cell type
    */
    function cell_type (cell) {
        if (is_extra_cell(cell)) {
            return cell.metadata.extended_cell.type;
        }
        return cell.cell_type;
    }

    /**
    * Overwrite the original to_markdown function
    * If an extra cell is turned from code to markdown
    * we need to make sure to unrender it fully
    */
    function patch_Notebook_to_markdown() {
        notebook.Notebook.prototype.to_markdown = function () {
            old_to_markdown.apply(this, arguments);
            let cell = this.get_cell(arguments[0]);
            cell.unrender_force();
            cell.render();
        };
    }

    /**
    * Overwrite the original toJSON function
    * If we have an attachment cell we want to keep all attachments
    * independent of whether they are referenced in the cell source
    * or not.
    */
    function patch_TextCell_toJSON() {
        TextCell.prototype.toJSON = function () {
            if (cell_type(this) == 'attachments') {
                // Do not remove ununsed attachments
                arguments[0] = false;
                return old_toJSON.apply(this, arguments);
            } else {
                return old_toJSON.apply(this, arguments);
            }
        }
    }

    /**
    * Overwrite the original render function of markdown cells
    */
    function patch_MarkdownCell_render () {
        MarkdownCell.prototype.render_force = old_render;

        MarkdownCell.prototype.render = function () {
            let type = cell_type(this);
            if (type == 'singlechoice') {
                let sc = new choice_cell.SinglechoiceCell(this);
                sc.edit_mode = edit_mode;
                sc.render();
            } else if (type == 'multiplechoice') {
                let mc = new choice_cell.MultiplechoiceCell(this);
                mc.edit_mode = edit_mode;
                mc.render();
            } else if (type == 'attachments') {
                let mycell = new attachment_cell.AttachmentCell(this);
                mycell.edit_mode = edit_mode;
                mycell.render();
            } else if (type == 'pdf') {
                let mycell = new pdf_cell.PDFCell(this);
                mycell.edit_mode = edit_mode;
                mycell.render();
            } else if (type == 'form') {
                let mycell = new form_cell.FormCell(this);
                mycell.edit_mode = edit_mode;
                mycell.render();
            } else {
                old_render.apply(this, arguments);
            }
        }
    }

    /**
    * Overwrite the original unrender function of markdown cells
    * Disables unrendering extra cells
    */
    function patch_MarkdownCell_unrender () {
        MarkdownCell.prototype.unrender_force = old_unrender;
        MarkdownCell.prototype.unrender = function () {
            if (!is_extra_cell(this)) {
                old_unrender.apply(this, arguments);
            }
        }
    }

    /**
    * Iterate over all cells and rerender extra cells
    */
    function render_extended_cells () {
        let cells = Jupyter.notebook.get_cells();
        for (let i in cells) {
            let cell = cells[i];
            if (is_extra_cell(cell) && cell.rendered) {
                cell.unrender_force();
                cell.render();
            }
        }
    }

    function load_css () {
        let link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.href = require.toUrl('./extra_cells.css');
        document.getElementsByTagName('head')[0].appendChild(link);
    }

    function initialize () {
        // Add special event handler when items are removed
        $.event.special.destroyed = {
            remove: function(o) {
                if (o.handler) {
                    o.handler()
                }
            }
        };

        load_css();
        if (Jupyter.notebook.metadata.hasOwnProperty('celltoolbar')) {
            if (Jupyter.notebook.metadata.celltoolbar == 'Create Assignment') {
                edit_mode = true;
            }
        }
        patch_TextCell_toJSON();
        patch_MarkdownCell_render();
        patch_MarkdownCell_unrender();
        patch_Notebook_to_markdown();
        render_extended_cells();
        events.on('preset_activated.CellToolbar', function (evt, preset) {
            console.log('Preset changed to '+preset.name);
            if (preset.name == 'Create Assignment') {
                edit_mode = true;
            } else {
                edit_mode = false;
            }
            render_extended_cells();
        });
        events.on('global_hide.CellToolbar', function (evt, instance) {
            edit_mode = false;
            render_extended_cells();
        });
    }

    let load_ipython_extension = function () {
        return Jupyter.notebook.config.loaded.then(initialize);
    };

    return {
        load_ipython_extension: load_ipython_extension
    };

});
