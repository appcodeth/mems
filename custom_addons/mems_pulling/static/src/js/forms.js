odoo.define('mems_pulling.forms', function (require) {
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var KanbanRenderer = require('web.KanbanRenderer');
    var FormRenderer = require('web.FormRenderer');

    FormRenderer.include({
        autofocus: function () {
            var self = this.state;
            if (self.model === 'mems.borrow') {
                var state = self.data.state;
                if (state == 'borrow' || state == 'cancel' || state == 'close') {
                    window.$('.o_form_button_edit').hide();
                    window.$('.o_form_button_create').hide();
                } else {
                    window.$('.o_form_button_edit').show();
                    window.$('.o_form_button_create').show();
                }
            }
            if (self.model === 'mems.restore') {
                var state = self.data.state;
                if (state == 'restore' || state == 'cancel' || state == 'close') {
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
