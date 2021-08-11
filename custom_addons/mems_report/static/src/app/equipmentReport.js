var table_result = $('#table-report');
var panel_result = $('#panel-report');
var beginHtml = table_result.html();

function hideReport() {
    table_result.hide();
    panel_result.hide();
}

function showReport() {
    table_result.show();
    panel_result.show();
}

function runReport() {
    var tr = '';
    var sum_active_count = 0;
    var sum_repair_count = 0;
    var sum_calibrate_count = 0;
    var sum_pm_count = 0;
    var sum_borrow_count = 0;
    var sum_inactive_count = 0;
    var sum_total_count = 0;

    $.ajax({
        url: '/api/equipment/all',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                sum_active_count += data.active_count;
                sum_repair_count += data.repair_count;
                sum_calibrate_count += data.calibrate_count;
                sum_pm_count += data.pm_count;
                sum_borrow_count += data.borrow_count;
                sum_inactive_count += data.inactive_count;
                sum_total_count += data.total_count;

                tr += '<tr>' +
                    '<td>' + data.code + '</td>' +
                    '<td>' + data.name + '</td>' +
                    '<td>' + data.categ_name + '</td>' +
                    '<td>' + (data.uom_name || '') + '</td>' +
                    '<td>' + data.brand_name + '/' + data.model_name + '</td>' +
                    '<td class="text-center">' + data.active_count + '</td>' +
                    '<td class="text-center">' + data.repair_count + '</td>' +
                    '<td class="text-center">' + data.calibrate_count + '</td>' +
                    '<td class="text-center">' + data.pm_count + '</td>' +
                    '<td class="text-center">' + data.borrow_count + '</td>' +
                    '<td class="text-center">' + data.inactive_count + '</td>' +
                    '<td class="text-center">' + data.total_count + '</td>' +
                    '</tr>';
            });
            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="5">รวม</th>' +
                '<th class="text-center">' + sum_active_count + '</th>' +
                '<th class="text-center">' + sum_repair_count + '</th>' +
                '<th class="text-center">' + sum_calibrate_count + '</th>' +
                '<th class="text-center">' + sum_pm_count + '</th>' +
                '<th class="text-center">' + sum_borrow_count + '</th>' +
                '<th class="text-center">' + sum_inactive_count + '</th>' +
                '<th class="text-center">' + sum_total_count + '</th>' +
                '</tr>';

            table_result.append('<tfoot>' + tr + '</tfoot>');
            showReport();
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

$('#btnClearReport').on('click', function () {
    table_result.html('');
    table_result.append(beginHtml);
    table_result.hide();
    runReport();
});

$('#btnShowReport').on('click', function () {
    table_result.html('');
    table_result.append(beginHtml);
    table_result.hide();
    runReport();
});

$(function () {
    hideReport();
});
