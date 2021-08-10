odoo.define('mems_purchase.forms', function(require) {
    var registry = require('web.field_registry');
    var KanbanRenderer = require('web.KanbanRenderer');
    var FormRenderer = require('web.FormRenderer');

    FormRenderer.include({
        _onClick: function () {
            if (this.mode === 'readonly') {
            }
        },
        autofocus: function() {
            var self = this.state;
            if (self.model === 'mems.rfq') {
                var state = self.data.state;
                if (state !== 'draft') {
                    window.$('.o_form_button_edit').hide();
                    window.$('.o_form_button_create').hide();
                } else {
                    window.$('.o_form_button_edit').show();
                    window.$('.o_form_button_create').show();
                }
            } else if (self.model === 'mems.purchase') {
                var state = self.data.state;
                if (state === 'paid' || state === 'cancel' || state === 'close') {
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
