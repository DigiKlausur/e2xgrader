define([
    'jquery',
    'base/js/dialog'
], function (
    $,
    dialog
) {

    class Observer {

        constructor() {

        }  
    
        notify(observable) {
            alert('Notified!');
        }
    }

    class Observable {
        
        constructor() {
            this.observers = [];
        }
        
        registerObserver(observer) {
            this.observers.push(observer);
        }
        
        notifyAll() {
            let that = this;
            this.observers.forEach(observer => observer.notify(that));
        }
        
    }

    class AttachmentGallery extends Observer {

        constructor(cell, model) {
            super();         
            this.cell = cell;
            this.model = model;
            model.registerObserver(this);
        }

        notify(model) {
            //alert('Notified the gallery!');
        }

        addThumbnail(attachment) {
            let that = this;
            let item = $('<div/>').addClass('gallery-item').attr('id', attachment.id);

            let removeItemBody = $('<div/>')
                .addClass('remove-file-modal')
                .append($('<p/>')
                    .append('Are you sure you want to delete the file ' + attachment.name + ' ?'));
            let removeItem = $('<i/>').addClass('fa fa-trash');
            removeItem.click(function () {
                dialog.modal({
                    body: removeItemBody,
                    buttons: {
                        'Delete': {class: 'button-delete',
                                   click: function() {
                                        that.model.removeAttachment(attachment.name);
                                        that.model.save();
                                        $('#' + attachment.id + '.gallery-item')[0].remove();
                                   }},
                        'Cancel': {}
                    }
                })
            });
            item.append(removeItem);

            let preview = $('<i/>')
                .addClass('fa fa-search-plus')
                .click(function() {
                    let downloadLink = document.createElement('a');
                    downloadLink.href = 'data:' + attachment.type + ';base64,' + attachment.data;
                    downloadLink.target = '_blank';
                    downloadLink.download = attachment.name;
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                });
            item.append(preview);
            let thumbnail = $('<div/>').addClass('thumbnail');
            let caption = $('<div/>').addClass('caption');
            caption.append($('<span/>').text(attachment.name));

            if (attachment.type.startsWith('image')) {
                let img = new Image();
                img.src = 'data:' + attachment.type + ';base64,' + attachment.data;
                thumbnail.append(img);
            }
            item.append(thumbnail).append(caption);
            return item;
        }

        getControls() {
            let controls = $('<div/>').addClass('attachment-controls');
            controls.append($('<button/>').append('Gallery'));
            controls.append($('<button/>').append('Webcam'));
            controls.append($('<input/>')
                                .attr('id', 'upload-attachments')
                                .attr('type', 'file')
                                .attr('accept', 'application/pdf,image/*')
                                .attr('multiple', 'multiple')
                                .change(() => this.uploadFiles()));
            return controls;
        }

        uploadFiles() {
            let input = $('#upload-attachments')[0];
            let that = this;

            
            Array.prototype.forEach.call(input.files, function(file) {
                //console.log(file.name);
                let reader = new FileReader();
                reader.readAsDataURL(file);

                reader.onload = function() {
                    let data = reader.result;
                    let name = file.name;
                    that.model.addAttachment(name, data);
                    $('.gallery-view').append(that.addThumbnail(that.model.getAttachment(name)));
                    that.model.save();
                }

                reader.onerror = function() {
                    console.log(reader.error);
                }
            });


        }

        open() {
            let body = $('<div/>').addClass('attachment-editor');
            let gallery = $('<div/>').addClass('gallery-view');
            body.append(gallery);
            body.append(this.getControls());
            let that = this;
            this.model.getAttachments().forEach(attachment => gallery.append(that.addThumbnail(attachment)));
            dialog.modal({
                keyboard_manager: Jupyter.keyboard_manager,
                title: 'Attachment Editor',
                body: body,
            });
        }

    }

    class AttachmentModel extends Observable {

        constructor(cell) {
            super();
            this.cell = cell;
            this.typePattern = new RegExp("data:([^;]*)");
            this.imagePattern = new RegExp("!\\[[^\(]+\\]\\(attachment:[^)]+\\)", "g");
            this.infoPattern = new RegExp("\n### You uploaded \\d+ attachments.\n\n", "g");
            this.attachments = {};
            this.load();
        }

        load() {
            Object.assign(this.attachments, this.cell.attachments);
        }

        save() {
            if (this.attachments !== undefined) {
                this.cell.attachments = this.attachments;
                console.log('Saved attachments.');

            } else {
                console.log('Attachments not defined.');
            }
            this.updateCell();
        }

        updateCell() {
            let cleaned = this.cell.get_text().replace(this.imagePattern, '');
            cleaned = cleaned.replace(this.infoPattern, '');
            let n_attachments = Object.keys(this.attachments).length;
            cleaned += '\n### You uploaded ' + n_attachments + ' attachments.\n\n'
            this.cell.set_text(cleaned);
            this.cell.unrender_force();
            this.cell.render();
        }

        addAttachment(key, dataUrl) {
            let type = this.typePattern.exec(dataUrl)[1];
            let data = dataUrl.replace('data:' + type + ';base64,', '');
            let present = false;
            this.getAttachments().forEach(attachment => present = present | data == attachment.data);
            console.log('PRESENT: ' + present);
            if (present == 0) {
                this.attachments[key] = {};
                this.attachments[key][type] = data;
                this.notifyAll();
            }
        }
        
        removeAttachment(key) {
            delete this.attachments[key];
            this.notifyAll();
        }

        getAttachment(key) {
            return {
                name: key,
                type: Object.keys(this.attachments[key])[0],
                data: Object.values(this.attachments[key])[0] 
            }
        }

        getAttachments() {
            let that = this;
            let attachments = [];
            let id = 0;
            Object.keys(this.attachments).forEach(function(key) {
                id += 1;
                attachments.push({
                    id: id,
                    name: key,
                    type: Object.keys(that.attachments[key])[0],
                    data: Object.values(that.attachments[key])[0]
                });
            });
            return attachments;
        }

        getImageNames() {
            let images = [];
            for (let key in this.cell.attachments) {
                let type = Object.keys(this.attachments[key])[0];
                if (type.startsWith('image/')) {
                    images.push(key);
                }            
            }
            return images;
        }

    }

    return {
        AttachmentModel: AttachmentModel,
        AttachmentGallery: AttachmentGallery
    };

});