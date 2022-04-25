define([], function() {

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
            this.postSaveHook();
        }

        postSaveHook() {
        	// Invoked after attachments are saved

        }

        hasAttachment(key) {
        	return key in this.attachments;
        }

        getAttachment(key) {
        	return {
                id: this.ids[key],
                name: key,
                type: Object.keys(this.attachments[key])[0],
                data: Object.values(this.attachments[key])[0] 
            }
        }

        setAttachment(key, dataUrl) {
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

        getAttachments() {
            let that = this;
            let attachments = [];
            Object.keys(this.attachments).forEach(function(key) {
                attachments.push(that.getAttachment(key));
            });
            return attachments;
        }
	}

	class AttachmentCellModel extends AttachmentModel {

		postSaveHook() {
			let cleaned = this.cell.get_text().replace(this.imagePattern, '');
            cleaned = cleaned.replace(this.infoPattern, '');
            let n_attachments = Object.keys(this.attachments).length;
            cleaned += '\n### You uploaded ' + n_attachments + ' attachments.\n\n'
            this.cell.set_text(cleaned);
            this.cell.unrender_force();
            this.cell.render();
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

	class DiagramCellModel extends AttachmentModel {

		postSaveHook() {
            this.cell.unrender_force();
            this.cell.render();
		}

	}

	return {
		AttachmentModel: AttachmentModel,
		AttachmentCellModel: AttachmentCellModel,
		DiagramCellModel: DiagramCellModel
	}

});