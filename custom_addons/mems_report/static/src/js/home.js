odoo.define('mems_report.report_home', function (require) {
  "use strict";

  var Widget = require('web.Widget');
  var core = require('web.core');

  var HomeAction = Widget.extend({
    template: 'Home',
    xmlDependencies: ['/mems_report/static/src/xml/home.xml'],
  });

  var DashboardAction = Widget.extend({
    template: 'Dashboard',
    xmlDependencies: ['/mems_report/static/src/xml/dashboard.xml'],
  });

  var EquipmentReportAction = Widget.extend({
    template: 'EquipmentReport',
    xmlDependencies: ['/mems_report/static/src/xml/equipmentReport.xml'],
  });

  core.action_registry.add('mems_dashboard_action', DashboardAction);
  core.action_registry.add('mems_home_action', HomeAction);
  core.action_registry.add('mems_equipment_report', EquipmentReportAction);

  return {
    HomeAction: HomeAction,
    DashboardAction: DashboardAction,
    EquipmentReportAction: EquipmentReportAction,
  }
});
