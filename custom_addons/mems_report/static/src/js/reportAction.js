odoo.define('mems_report.report_action', function(require) {
    "use strict";
    var Widget = require('web.Widget');
    var core = require('web.core');

    // Equipment
    var EquipmentStatusReportAction = Widget.extend({
        template: 'EquipmentStatusReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentStatusReport.xml'],
    });

    var EquipmentCalibrateReportAction = Widget.extend({
        template: 'EquipmentCalibrateReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentCalibrateReport.xml'],
    });

    var EquipmentPmReportAction = Widget.extend({
        template: 'EquipmentPmReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentPmReport.xml'],
    });

    var EquipmentDowntimeReportAction = Widget.extend({
        template: 'EquipmentDowntimeReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentDowntimeReport.xml'],
    });

    var EquipmentWarrantyReportAction = Widget.extend({
        template: 'EquipmentWarrantyReport',
        xmlDependencies: ['/mems_report/static/src/xml/equipmentWarrantyReport.xml'],
    });

    // Inventory
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

    var InventoryIssueReportAction = Widget.extend({
        template: 'InventoryIssueReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryIssueReport.xml'],
    });

    var InventoryPurchaseReportAction = Widget.extend({
        template: 'InventoryPurchaseReport',
        xmlDependencies: ['/mems_report/static/src/xml/inventoryPurchaseReport.xml'],
    });

    // Pulling
    var PullingBorrowReportAction = Widget.extend({
        template: 'PullingBorrowReport',
        xmlDependencies: ['/mems_report/static/src/xml/pullingBorrowReport.xml'],
    });

    var PullingRestoreReportAction = Widget.extend({
        template: 'PullingRestoreReport',
        xmlDependencies: ['/mems_report/static/src/xml/pullingRestoreReport.xml'],
    });

    var PullingOverdateReportAction = Widget.extend({
        template: 'PullingOverdateReport',
        xmlDependencies: ['/mems_report/static/src/xml/pullingOverdateReport.xml'],
    });

    // staff
    var StaffPerformanceReportAction = Widget.extend({
        template: 'StaffPerformanceReport',
        xmlDependencies: ['/mems_report/static/src/xml/staffPerformanceReport.xml'],
    });

    // repair
    var RepairWorkorderReportAction = Widget.extend({
        template: 'RepairWorkorderReport',
        xmlDependencies: ['/mems_report/static/src/xml/repairWorkorderReport.xml'],
    });

    var RepairOverdateAction = Widget.extend({
        template: 'RepairOverdateReport',
        xmlDependencies: ['/mems_report/static/src/xml/repairOverdateReport.xml'],
    });

    core.action_registry.add('mems_equipment_status_report', EquipmentStatusReportAction);
    core.action_registry.add('mems_equipment_calibrate_report', EquipmentCalibrateReportAction);
    core.action_registry.add('mems_equipment_pm_report', EquipmentPmReportAction);
    core.action_registry.add('mems_equipment_downtime_report', EquipmentDowntimeReportAction);
    core.action_registry.add('mems_equipment_warranty_report', EquipmentWarrantyReportAction);
    core.action_registry.add('mems_inventory_balance_report', InventoryBalanceReportAction);
    core.action_registry.add('mems_inventory_move_report', InventoryMoveReportAction);
    core.action_registry.add('mems_inventory_low_report', InventoryLowReportAction);
    core.action_registry.add('mems_inventory_topuse_report', InventoryTopUseReportAction);
    core.action_registry.add('mems_inventory_receive_report', InventoryReceiveReportAction);
    core.action_registry.add('mems_inventory_issue_report', InventoryIssueReportAction);
    core.action_registry.add('mems_inventory_purchase_report', InventoryPurchaseReportAction);
    core.action_registry.add('mems_pulling_borrow_report', PullingBorrowReportAction);
    core.action_registry.add('mems_pulling_restore_report', PullingRestoreReportAction);
    core.action_registry.add('mems_pulling_overdate_report', PullingOverdateReportAction);
    core.action_registry.add('mems_staff_performance_report', StaffPerformanceReportAction);
    core.action_registry.add('mems_repair_workorder_report', RepairWorkorderReportAction);
    core.action_registry.add('mems_repair_overdate_report', RepairOverdateAction);
    return {};
});
