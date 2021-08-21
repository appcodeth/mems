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
        url: '/api/equipment/status',
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
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td>' + data.name + '</td>' +
                    '<td>' + data.categ_name + '</td>' +
                    '<td>' + (data.uom_name || '') + '</td>' +
                    '<td>' + data.brand_name + '/' + data.model_name + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.active_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.repair_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.calibrate_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.pm_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.borrow_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.inactive_count, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.total_count, 0) + '</td>' +
                    '</tr>';
            });
            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="5">รวม</th>' +
                '<th class="text-center">' + numberWithCommas(sum_active_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_repair_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_calibrate_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_pm_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_borrow_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_inactive_count, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_total_count, 0) + '</th>' +
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
