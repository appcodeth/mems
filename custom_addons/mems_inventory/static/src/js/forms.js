odoo.define('mems_inventory.forms', function (require) {
    var registry = require('web.field_registry');
    var KanbanRenderer = require('web.KanbanRenderer');
    var FormRenderer = require('web.FormRenderer');
    FormRenderer.include({
        autofocus: function () {
            var self = this.state;
            if(self.model === 'mems.receive'){
                var state = self.data.state;
                if(state == 'complete' || state == 'cancel') {
                    window.$('.o_form_button_edit').hide();
                    window.$('.o_form_button_create').hide();
                } else {
                    window.$('.o_form_button_edit').show();
                    window.$('.o_form_button_create').show();
                }
            } else if(self.model === 'mems.issue'){
                var state = self.data.state;
                if(state == 'complete' || state == 'cancel') {
                    window.$('.o_form_button_edit').hide();
                    window.$('.o_form_button_create').hide();
                } else {
                    window.$('.o_form_button_edit').show();
                    window.$('.o_form_button_create').show();
                }
            } else if(self.model === 'mems.return'){
                var state = self.data.state;
                if(state == 'complete' || state == 'cancel') {
                    window.$('.o_form_button_edit').hide();
                    window.$('.o_form_button_create').hide();
                } else {
                    window.$('.o_form_button_edit').show();
                    window.$('.o_form_button_create').show();
                }
            }
            return this._super();
        },
    });
    return {};
});
