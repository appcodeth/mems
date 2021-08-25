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
    $.ajax({
        url: '/api/pulling/overdate',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td>' + (data.code || '') + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td>' + (data.brand_name || '') + ' / ' + (data.model_name || '') + '</td>' +
                    '<td>' + (data.serial_no || '') + '</td>' +
                    '<td>' + (data.borrow_name || '') + '</td>' +
                    '<td>' + (data.dept_name || '') + '</td>' +
                    '<td class="text-center">' + (data.borrow_date || '') + '</td>' +
                    '<td class="text-center">' + (data.expect_date || '') + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.no_day, 0) + '</td>' +
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
