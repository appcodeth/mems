odoo.define('mems_report.report_action', function(require) {
    "use strict";
    var Widget = require('web.Widget');
    var core = require('web.core');

    var EquipmentStatusReportAction = Widget.extend({
        template: 'EquipmentStatusReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentStatusReport.xml'],
    });

    var InventoryBalanceReportAction = Widget.extend({
        template: 'InventoryBalanceReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryBalanceReport.xml'],
    });

    core.action_registry.add('mems_equipment_status_report', EquipmentStatusReportAction);
    core.action_registry.add('mems_inventory_balance_report', InventoryBalanceReportAction);
    return {};
});
