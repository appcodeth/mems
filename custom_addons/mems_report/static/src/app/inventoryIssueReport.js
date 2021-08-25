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
        url: '/api/inventory/issue?start_date=' + start_date + '&end_date=' + end_date,
        type: 'get',
        async: false,
        success: function (res) {
            var count = 0;
            var temp_code = '';
            var total_qty = 0;
            var total_price = 0;
            var total_amount = 0;

            $.each(res.rows, function (index, data) {
                var sep = '';
                if(temp_code != data.code) {
                    var sum_tr = '';
                    if(index > 0) {
                        sum_tr = '<tr>' +
                            '<th colspan="7">รวม</th>' +
                            '<th class="text-center">' + numberWithCommas(total_qty, 0) + '</th>' +
                            '<th class="text-right">' + numberWithCommas(total_price, 2) + '</th>' +
                            '<th class="text-right">' + numberWithCommas(total_amount, 2) + '</th>' +
                        '</tr>';
                    }

                    sep = sum_tr + '<tr style="color:#369"><td colspan="20"><strong>[' + data.code + '] ' + data.name + '</strong></td></tr>';
                    temp_code = data.code;
                    count = 1;
                    total_qty = data.qty;
                    total_price = data.price;
                    total_amount = data.amount;
                } else {
                    count += 1;
                    total_qty += data.qty;
                    total_price += data.price;
                    total_amount += data.amount;
                }

                tr += sep + '<tr>' +
                    '<td class="text-center">' + count + '</td>' +
                    '<td>' + data.issue_date + '</td>' +
                    '<td>' + data.issue_name + '</td>' +
                    '<td>' + (data.wo_name || '') + '</td>' +
                    '<td>' + (data.wo_date || '') + '</td>' +
                    '<td>' + (data.dept_name || '') + '</td>' +
                    '<td>' + (data.uom_name || '') + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.qty, 0) + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.price, 2) + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.amount, 2) + '</td>' +
                    '</tr>';
            });

            // make tbody last data
            tr += '<tr>' +
                '<th colspan="7">รวม</th>' +
                '<th class="text-center">' + numberWithCommas(total_qty, 0) + '</th>' +
                '<th class="text-right">' + numberWithCommas(total_price, 2) + '</th>' +
                '<th class="text-right">' + numberWithCommas(total_amount, 2) + '</th>' +
            '</tr>';

            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');
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
