import { TextCell, MarkdownCell } from "notebook/js/textcell";
import { utils } from "@e2xgrader/cells";
import markdown from "base/js/markdown";

const old_render = MarkdownCell.prototype.render;
const old_unrender = MarkdownCell.prototype.unrender;

/**
 * Add a new unsafe renderer for markdown cells to render dynamic content
 */
export function add_unsafe_renderer() {
  MarkdownCell.prototype.unsafe_render = function () {
    this.drag_counter = 0;
    this.inner_cell.removeClass("dropzone");

    let cont = TextCell.prototype.render.apply(this);
    if (cont) {
      let that = this;
      let text = this.get_text();
      if (text === "") {
        text = this.placeholder;
      }

      markdown.render(
        text,
        {
          with_math: true,
          clean_tables: true,
          sanitize: false,
        },
        function (err, html) {
          html = $(html);
          // add anchors to headings
          html
            .find(":header")
            .addBack(":header")
            .each(function (i, h) {
              h = $(h);
              let hash = h.text().replace(/ /g, "-");
              h.attr("id", hash);
              h.append(
                $("<a/>")
                  .addClass("anchor-link")
                  .attr("href", "#" + hash)
                  .text("¶")
                  .on("click", function () {
                    setTimeout(function () {
                      that.unrender();
                      that.render();
                    }, 100);
                  })
              );
            });
          // links in markdown cells should open in new tabs
          html.find("a[href]").not('[href^="#"]').attr("target", "_blank");
          // replace attachment:<key> by the corresponding entry
          // in the cell's attachments
          html.find('img[src^="attachment:"]').each(function (i, h) {
            h = $(h);
            let key = h.attr("src").replace(/^attachment:/, "");

            if (that.attachments.hasOwnProperty(key)) {
              let att = that.attachments[key];
              let mime = Object.keys(att)[0];
              h.attr("src", "data:" + mime + ";base64," + att[mime]);
            } else {
              h.attr("src", "");
            }
          });
          that.set_rendered(html);
          that.typeset();
          that.events.trigger("rendered.MarkdownCell", {
            cell: that,
          });
        }
      );
    }
    return cont;
  };
}

export function patch_MarkdownCell_render() {
  MarkdownCell.prototype.render_force = old_render;
}

export function patch_MarkdownCell_unrender() {
  MarkdownCell.prototype.unrender_force = old_unrender;
  MarkdownCell.prototype.unrender = function () {
    if (!utils.is_e2x(this)) {
      old_unrender.apply(this, arguments);
    }
  };
}
