define([
    'jquery',
    'base/js/dialog'
], function (
    $,
    dialog
) {

    class Observer {
    
        notify(observable) {
            
        }
    }

    class Observable {
        
        constructor() {
            this.observers = [];
        }
        
        registerObserver(observer) {
            this.observers.push(observer);
        }
        
        notifyAll(event) {
            this.observers.forEach(observer => observer.notify(event));
        }
        
    }

    class Webcam {

        constructor(model) {
            this.stream = undefined;
            this.model = model;
        }

        open() {
        	let that = this;
	        let videoObj = { "video": true };
	        navigator.mediaDevices.getUserMedia(videoObj).then(
                function sucess(stream) {
    	        	that.stream = stream;
    	        	that.openDialog();
    	        }).catch(function(err) {
                    alert('Could not access webcam!\n' + err);
                }
            );
        }

        openDialog() {
        	let that = this;
        	let body = $('<div/>').attr('id', 'webcamDiv');
	        let video = $('<video/>');
	        body.append(video);

	        let controls = $('<div/>').attr('id', 'videoControls');
	        controls.append($('<button/>')
	                        .attr('id', 'takePhoto')
	                        .click(() => {
	                            if (video[0].paused) {
	                                video[0].play();
	                                $('#saveImage').attr('disabled', true);
	                                $('#takePhoto span').text('Take Photo');
	                            } else {
	                                video[0].pause();
	                                $('#saveImage').removeAttr('disabled');
	                                $('#takePhoto span').text('Retry');
	                            }
	                        })
	                        .append($('<span/>').text('Take Photo')));
	        body.append(controls);  

	        dialog.modal({
	            keyboard_manager: Jupyter.keyboard_manager,
	            title: 'Take Photo',
	            open: () => {
	                
	                $('#webcamDiv').bind('destroyed', function() {
	                    that.close();
	                });
	            },
	            body: body,
	            buttons: {
	                'Save Image': {
	                    id: 'saveImage',
	                    click: () => {
	                        let tmpCanvas = $('<canvas/>').attr('width', video[0].videoWidth).attr('height', video[0].videoHeight);
	                        tmpCanvas[0].getContext('2d').drawImage(video[0], 0, 0, video[0].videoWidth, video[0].videoHeight);
	                        let dataUrl = tmpCanvas[0].toDataURL('image/png');
	                        let key = that.model.getName('webcam', 'png');
	                        that.model.addAttachment(key, dataUrl);
	                    }
	                },
	                Cancel: {}
	            }
	        });

	        if (navigator.getUserMedia || navigator.mozGetUserMedia) {
	            video[0].srcObject = that.stream;
	            video[0].play();
	        } else if (navigator.webkitGetUserMedia) {        // WebKit
	            video[0].src = window.webkitURL.createObjectURL(stream);
	            video[0].play();
	        } 
        }

        close() {
        	if (this.stream !== undefined) {
        		this.stream.getTracks().forEach(track => track.stop());
        	}

        }


    }

    class AttachmentGallery extends Observer {

        constructor(cell, model) {
            super();         
            this.cell = cell;
            this.model = model;
            this.element = $('<div/>').addClass('gallery-view');
            model.registerObserver(this);
        }

        notify(event) {
            if (event.type == 'delete') {
                this.element.find($('#' + event.id)).remove();
            } else if (event.type == 'add') {
                this.addThumbnail(this.model.getAttachment(event.key));
            }
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
                                   click: () => that.model.removeAttachment(attachment.name)},
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
            this.element.append(item);
        }

        getControls() {
            let controls = $('<div/>').addClass('attachment-controls');
            
            controls.append($('<button/>')
                .append($('<i/>').addClass('fa fa-camera'))
                .append('Webcam')
                .click(() => new Webcam(this.model).open()));
            let input_button = $('<button/>')
                .addClass('upload-btn')
                .append($('<i/>').addClass('fa fa-upload'))
                .append('Upload')
                .click(() => $('#upload-attachments')[0].click());
            
            input_button.append($('<input/>')
                                .attr('id', 'upload-attachments')
                                .attr('type', 'file')
                                .attr('accept', 'application/pdf,image/*')
                                .attr('multiple', 'multiple')
                                .change(() => this.uploadFiles()));

            controls.append(input_button);
            return controls;
        }

        uploadFiles() {
            let input = $('#upload-attachments')[0];
            let that = this;

            
            Array.prototype.forEach.call(input.files, function(file) {
                let reader = new FileReader();
                reader.readAsDataURL(file);

                reader.onload = function() {
                    let data = reader.result;
                    let key = file.name;
                    if (!that.model.addAttachment(key, data)) {
                        let name = key.split('.')[0];
                        let type = key.replace(name + '.', '');
                        let newName = that.model.getName(name, type);

                        let msg = 'A file with the name ' + key + ' already exists!\nDo you want to rename it to ' + newName + '?'

                        if (confirm(msg)) {
                            that.model.addAttachment(newName, data);
                        }

                        
                    }                    
                }

                reader.onerror = function() {
                    console.log(reader.error);
                }
            });


        }

        open() {
            let body = $('<div/>').addClass('attachment-editor');
            this.element = $('<div/>').addClass('gallery-view');
            body.append(this.element);
            body.append(this.getControls());
            let that = this;
            this.model.getAttachments().forEach(attachment => that.addThumbnail(attachment));
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
            this.ids = {};
            this.cell = cell;
            this.typePattern = new RegExp("data:([^;]*)");
            this.imagePattern = new RegExp("!\\[[^\(]+\\]\\(attachment:[^)]+\\)", "g");
            this.infoPattern = new RegExp("\n### You uploaded \\d+ attachments.\n\n", "g");
            this.attachments = {};            
            this.load();
        }

        load() {
            let that = this;
            this.id = 0;
            Object.assign(this.attachments, this.cell.attachments);
            Object.keys(this.attachments).forEach(function(key) {
                that.id += 1;
                that.ids[key] = that.id;                
            });
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
            if (key in this.attachments) {
                return false;
            }
            let type = this.typePattern.exec(dataUrl)[1];
            let data = dataUrl.replace('data:' + type + ';base64,', '');
            this.id += 1;
            this.attachments[key] = {};
            this.attachments[key][type] = data;
            this.ids[key] = this.id;
            this.notifyAll({
                type: 'add',
                key: key,
                id: this.ids[key]
            });
            this.save();
            return true;
        }
        
        removeAttachment(key) {
            let id = this.ids[key];
            delete this.attachments[key];
            delete this.ids[key];
            this.notifyAll({
                type: 'delete',
                key: key,
                id: id
            });
            this.save();
        }

        getAttachment(key) {
            return {
                id: this.ids[key],
                name: key,
                type: Object.keys(this.attachments[key])[0],
                data: Object.values(this.attachments[key])[0] 
            }
        }

        getAttachments() {
            let that = this;
            let attachments = [];
            Object.keys(this.attachments).forEach(function(key) {
                attachments.push(that.getAttachment(key));
            });
            return attachments;
        }

        getName(name, type) {
            let current_name = name + '.' + type;
            let counter = 0;
            while (current_name in this.attachments) {
                counter += 1;
                current_name = name + '_' + counter + '.' + type;
            }
            return current_name;
        }

    }

    return {
        AttachmentModel: AttachmentModel,
        AttachmentGallery: AttachmentGallery
    };

});
