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
    var sum_stock_qty = 0;

    $.ajax({
        url: '/api/inventory/topuse',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                sum_stock_qty += data.qty;
                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td class="text-center">' + (data.code || '') + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td>' + (data.categ_name || '') + '</td>' +
                    '<td>' + (data.uom_name || '') + '</td>' +
                    '<td>' + (data.brand_name || '') + '</td>' +
                    '<td>' + (data.loc_name || '') + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.qty, 0) + '</td>' +
                    '</tr>';
            });
            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="7">รวม</th>' +
                '<th class="text-center">' + numberWithCommas(sum_stock_qty, 0) + '</th>' +
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
