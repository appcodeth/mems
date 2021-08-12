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
    var str_start = $('#from_date').val();
    var str_end = $('#end_date').val();

    if (str_start && str_end);
    else {
        alert('Please select date');
        return;
    }

    var start_date = getDate(str_start);
    var end_date = getDate(str_end);
    var tr = '';
    var sum_stock_qty = 0;
    var sum_cost_price = 0;
    var sum_total_cost = 0;

    $.ajax({
        url: '/api/pulling/borrow?start_date=' + start_date + '&end_date=' + end_date,
        type: 'get',
        async: false,
        success: function (res) {
            var total_qty = 0;

            $.each(res.rows, function (index, data) {
                total_qty += data.qty;

                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td class="text-center">' + (data.name || '') + '</td>' +
                    '<td class="text-center">' + (data.borrow_date || '') + '</td>' +
                    '<td class="text-center">' + (data.expect_date || '') + '</td>' +
                    '<td class="text-center">' + (data.no_day || '') + '</td>' +
                    '<td>' + (data.dept_name || '') + '</td>' +
                    '<td class="text-center">' + (data.code || '') + '</td>' +
                    '<td>' + (data.equip_name || '') + '</td>' +
                    '<td class="text-center">' + (data.brand_name || '') + '</td>' +
                    '<td class="text-center">' + (data.model_name || '') + '</td>' +
                    '<td class="text-center">' + (data.serial_no || '') + '</td>' +
                    '<td class="text-center">' + (data.login || '') + '</td>' +
                    '<td class="text-center">' + (data.qty || '') + '</td>' +
                '</tr>';
            });

            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="12">รวม</th>' +
                '<th class="text-center">' + numberWithCommas(total_qty, 0) + '</th>' +
            '</tr>';

            table_result.append('<tfoot>' + tr + '</tfoot>');
            showReport();
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

function getCurrentDate() {
    var today = new Date();

    var day = twoDigitsNumber(1);
    var month = twoDigitsNumber(today.getMonth() + 1);
    var year = today.getFullYear();
    var last_day = twoDigitsNumber(getLastDay(year, today.getMonth()));

    $('#from_date').val(day + '/' + month + '/' + year);
    $('#end_date').val(last_day + '/' + month + '/' + year);
}

$('#btnClearReport').on('click', function () {
    table_result.html('');
    table_result.append(beginHtml);
    hideReport();
    getCurrentDate();
    runReport();
});

$('#btnShowReport').on('click', function () {
    table_result.html('');
    table_result.append(beginHtml);
    hideReport();
    runReport();
});

$(function () {
    $('.datepicker').datepicker({
        language: 'th',
        orientation: 'auto bottom',
        format: 'dd/mm/yyyy',
        todayHighlight: true,
    });

    hideReport();
    getCurrentDate();
});
