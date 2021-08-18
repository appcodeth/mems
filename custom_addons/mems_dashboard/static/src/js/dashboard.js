odoo.define('mems_dashboard.dashboard', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var core = require('web.core');

    var DashboardAction = Widget.extend({
        template: 'DashboardOverview',
        xmlDependencies: ['/mems_dashboard/static/src/xml/dashboard.xml'],
    });

    var PricingTableAction = Widget.extend({
        template: 'PricingTable',
        xmlDependencies: ['/mems_dashboard/static/src/xml/pricing.xml'],
    });

    var ManualDownloadAction = Widget.extend({
        template: 'ManualDownload',
        xmlDependencies: ['/mems_dashboard/static/src/xml/manual.xml'],
    });

    var VideoSuggestionAction = Widget.extend({
        template: 'VideoSuggestion',
        xmlDependencies: ['/mems_dashboard/static/src/xml/video.xml'],
    });

    core.action_registry.add('dashboard_overview', DashboardAction);
    core.action_registry.add('pricing_table_overview', PricingTableAction);
    core.action_registry.add('manual_download_overview', ManualDownloadAction);
    core.action_registry.add('video_suggest_overview', VideoSuggestionAction);

    return {};
});
