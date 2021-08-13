odoo.define('mems_dashboard.dashboard', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');

    var DashboardAction = Widget.extend({
        template: 'DashboardOverview',
        xmlDependencies: ['/mems_dashboard/static/src/xml/dashboard.xml'],
    });

    core.action_registry.add('dashboard_overview', DashboardAction);

    return {
        DashboardAction: DashboardAction,
    }
});
