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
        url: '/api/repair/workorder',
        type: 'get',
        async: false,
        success: function (res) {
            var sum_approve = 0;
            var sum_completed = 0;
            var sum_closed = 0;

            $.each(res.rows, function (index, data) {
                sum_approve += (data.approved || 0);
                sum_completed += (data.completed || 0);
                sum_closed += (data.closed || 0);

                tr += '<tr>' +
                    '<td class="text-center">' + (data.name || '') + '</td>' +
                    '<td class="text-center">' + (data.date_order || '') + '</td>' +
                    '<td>' + ('[' + data.eq_code + '] ' + data.eq_name) + '</td>' +
                    '<td class="text-center">' + (data.eq_brand + '/' + data.eq_model) + '</td>' +
                    '<td class="text-center">' + (data.eq_sn || '') + '</td>' +
                    '<td>' + (data.problem_text || '') + '</td>' +
                    '<td>' + (data.service_type == 'by_vendor' ? 'บริษัทภายนอก' : 'ทีมช่าง') + '</td>' +
                    '<td>' + (data.service_type=='by_vendor' ? data.sup_name : data.login) + '</td>' +
                    '<td class="text-center">' + (data.approved ? '<i class="fa fa-check"></i>' : '') + '</td>' +
                    '<td class="text-center">' + (data.completed ? '<i class="fa fa-check"></i>' : '') + '</td>' +
                    '<td class="text-center">' + (data.closed ? '<i class="fa fa-check"></i>' : '') + '</td>' +
                '</tr>';
            });
            // make tbody data
            table_result.append('<tbody>' + tr + '</tbody>');

            // make tfoot data
            tr = '<tr>' +
                '<th colspan="8">รวม ' + numberWithCommas(sum_approve + sum_completed + sum_closed, 0) + ' งาน</th>' +
                '<th class="text-center">' + numberWithCommas(sum_approve, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_completed, 0) + '</th>' +
                '<th class="text-center">' + numberWithCommas(sum_closed, 0) + '</th>' +
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
