odoo.define('mems_master.widgets', function(require) {
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');
    var KanbanRenderer = require('web.KanbanRenderer');

    var LabelStatusWidget = AbstractField.extend({
        _render: function() {
            var cssClass = '';
            var text = '';
            if (this.model === 'mems.equipment') {
                if (this.value === 'active') {
                    cssClass = 'status-success';
                    text = 'พร้อมใช้';
                } else if (this.value === 'pm') {
                    cssClass = 'status-warning';
                    text = 'บำรุงรักษา';
                } else if (this.value === 'calibrate') {
                    cssClass = 'status-warning';
                    text = 'สอบเทียบ';
                } else if (this.value === 'borrow') {
                    cssClass = 'status-warning';
                    text = 'ยืม';
                } else if (this.value === 'repair') {
                    cssClass = 'status-warning';
                    text = 'ซ่อม';
                } else if (this.value === 'inactive') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                }
            } else if (this.model === 'mems.pm' || this.model === 'mems.calibration') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'approve') {
                    cssClass = 'status-success';
                    text = 'อนุมัติ';
                } else if (this.value === 'close') {
                    cssClass = 'status-info';
                    text = 'เสร็จสิ้น';
                }
            } else if (this.model === 'mems.rfq') {
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'approve') {
                    cssClass = 'status-success';
                    text = 'อนุมัติ';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                }
            } else if (this.model === 'mems.purchase') {
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'approve') {
                    cssClass = 'status-info';
                    text = 'อนุมัติ';
               } else if (this.value === 'paid') {
                    cssClass = 'status-success';
                    text = 'ชำระเงินแล้ว';
                } else if (this.value === 'close') {
                    cssClass = 'status-default';
                    text = 'จบงาน';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                }
            } else if (this.model === 'mems.borrow') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'borrow') {
                    cssClass = 'status-success';
                    text = 'ยืม';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                } else if (this.value === 'close') {
                    cssClass = 'status-info';
                    text = 'คืนแล้ว';
                }
            } else if (this.model === 'mems.restore') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'restore') {
                    cssClass = 'status-success';
                    text = 'คืน';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                } else if (this.value === 'close') {
                    cssClass = 'status-info';
                    text = 'จบการคืน';
                }
            } else if(this.model === 'mems.sr') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'approve') {
                    cssClass = 'status-info';
                    text = 'ส่งซ่อม';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                } else if (this.value === 'close') {
                    cssClass = 'status-default';
                    text = 'จบงาน';
                }
            } else if (this.model === 'mems.workorder') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'approve') {
                    cssClass = 'status-info';
                    text = 'ซ่อม';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                } else if (this.value === 'vendor') {
                    cssClass = 'status-info';
                    text = 'ส่งซ่อม';
                } else if (this.value === 'complete') {
                    cssClass = 'status-success';
                    text = 'ซ่อมเสร็จ';
                } else if (this.value === 'close') {
                    cssClass = 'status-default';
                    text = 'จบงาน';
                }
            } else if (this.model === 'mems.receive' || this.model === 'mems.issue' || this.model === 'mems.return') {
                cssClass = '';
                text = '';
                if (this.value === 'draft') {
                    cssClass = 'status-warning';
                    text = 'รออนุมัติ';
                } else if (this.value === 'complete') {
                    cssClass = 'status-success';
                    text = 'สำเร็จ';
                } else if (this.value === 'cancel') {
                    cssClass = 'status-danger';
                    text = 'ยกเลิก';
                }
            }
            this.$el.html('<span class="status ' + cssClass + '">' + text + '</span>');
        }
    });

    registry.add('labelStatus', LabelStatusWidget);
    return {};
});
