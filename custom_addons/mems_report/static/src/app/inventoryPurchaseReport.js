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
        url: '/api/inventory/purchase?start_date=' + start_date + '&end_date=' + end_date,
        type: 'get',
        async: false,
        success: function (res) {
            var state = '';
            var total_untaxed = 0;
            var total_tax = 0;
            var total_amount = 0;

            $.each(res.rows, function (index, data) {
                total_untaxed += data.amount_untaxed;
                total_tax += data.amount_tax;
                total_amount += data.amount_total;

                if (data.state === 'draft') {
                    state = 'รออนุมัติ';
                } else if (data.state === 'approve') {
                    state = 'อนุมัติ';
                } else if (data.state === 'paid') {
                    state = 'ชำระเงินแล้ว';
                } else if (data.state === 'close') {
                    state = 'ปิด';
                } else if (data.state === 'cancel') {
                    state = 'ยกเลิก';
                }

                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td>' + (data.date_order || '') + '</td>' +
                    '<td>' + (data.ref_rfq || '') + '</td>' +
                    '<td>' + (data.sup_name || '') + '</td>' +
                    '<td>' + (data.date_payment || '') + '</td>' +
                    '<td class="text-center">' + (state || '') + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.amount_untaxed, 2) + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.amount_tax, 2) + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.amount_total, 2) + '</td>' +
                '</tr>';
            });

            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="7">รวม</th>' +
                '<th class="text-right">' + numberWithCommas(total_untaxed, 2) + '</th>' +
                '<th class="text-right">' + numberWithCommas(total_tax, 2) + '</th>' +
                '<th class="text-right">' + numberWithCommas(total_amount, 2) + '</th>' +
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
