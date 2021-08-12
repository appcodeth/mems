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

    var InventoryMoveReportAction = Widget.extend({
        template: 'InventoryMoveReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryMoveReport.xml'],
    });

    var InventoryLowReportAction = Widget.extend({
        template: 'InventoryLowReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryLowReport.xml'],
    });

    var InventoryTopUseReportAction = Widget.extend({
        template: 'InventoryTopUseReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryTopUseReport.xml'],
    });

    var InventoryReceiveReportAction = Widget.extend({
        template: 'InventoryReceiveReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryReceiveReport.xml'],
    });

    core.action_registry.add('mems_equipment_status_report', EquipmentStatusReportAction);
    core.action_registry.add('mems_inventory_balance_report', InventoryBalanceReportAction);
    core.action_registry.add('mems_inventory_move_report', InventoryMoveReportAction);
    core.action_registry.add('mems_inventory_low_report', InventoryLowReportAction);
    core.action_registry.add('mems_inventory_topuse_report', InventoryTopUseReportAction);
    core.action_registry.add('mems_inventory_receive_report', InventoryReceiveReportAction);
    return {};
});
