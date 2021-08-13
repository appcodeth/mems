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
    var sum_total_work = 0;
    var sum_total_complete = 0;
    var sum_total_close = 0;

    $.ajax({
        url: '/api/staff/performance',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                sum_total_work += data.total_work;
                sum_total_complete += data.total_complete;
                sum_total_close += data.total_close;

                tr += '<tr>' +
                    '<td class="text-center">' + (index + 1) + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td>' + (data.email || '') + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.total_work, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.total_complete, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.total_close, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas((data.total_complete/data.total_work)*100, 1) + '</td>' +
                    '</tr>';
            });
            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="3">รวม</th>' +
                '<th class="text-center">' + numberWithCommas(sum_total_work, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_total_complete, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_total_close, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas((sum_total_complete/sum_total_work)*100, 1) + '</th>' +
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
