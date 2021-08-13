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
        url: '/api/equipment/calibrate?start_date=' + start_date + '&end_date=' + end_date,
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td class="text-center">' + (data.ca_name || '') + '</td>' +
                    '<td class="text-center">' + (data.start_date || '') + '</td>' +
                    '<td class="text-center">' + (data.end_date || '') + '</td>' +
                    '<td>' + (data.sup_name || '') + '</td>' +
                    '<td class="text-center">' + (data.code || '') + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td class="text-center">' + (data.categ_name || '') + '</td>' +
                    '<td class="text-center">' + (data.brand_name || '') + ' / ' + (data.model_name || '') + '</td>' +
                    '<td class="text-center">' + (data.serial_no || '') + '</td>' +
                    '<td class="text-center">' + (data.login || '') + '</td>' +
                '</tr>';
            });

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
