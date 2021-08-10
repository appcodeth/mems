odoo.define('mems_repair.custom_widget', function (require) {
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var KanbanRenderer = require('web.KanbanRenderer');

    var FormRenderer = require('web.FormRenderer');
    FormRenderer.include({
        autofocus: function () {
            var self = this.state;
            if(self.model === 'mems.workorder'){
                var state = self.data.state;
                if(state == 'close' || state == 'cancel') {
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

    KanbanRenderer.include({
        _setState: function (state) {
            var self = this;
            this._super(state);
            if (this.arch.attrs.sortable) {
                this.columnOptions = _.extend(self.columnOptions, {
                    sortable: this.arch.attrs.sortable === 'true',
                });
            }

            if (this.arch.attrs.disable_drag_drop_record) {
                if (this.arch.attrs.disable_drag_drop_record=='true') {
                    this.columnOptions.draggable = false;
                }
            }
        },

        _renderGrouped: function (fragment) {
            this._super.apply(this, arguments);
            if (this.columnOptions.sortable===false) {
                this.$el.sortable('destroy');
            }
        },
    });

    return {};
});
