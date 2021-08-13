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
        url: '/api/repair/overdate',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                tr += '<tr>' +
                    '<td class="text-center">' + (data.name || '') + '</td>' +
                    '<td class="text-center">' + (data.date_order || '') + '</td>' +
                    '<td class="text-center">' + (data.date_plan || '') + '</td>' +
                    '<td>' + ('[' + data.eq_code + '] ' + data.eq_name) + '</td>' +
                    '<td class="text-center">' + (data.eq_brand + '/' + data.eq_model) + '</td>' +
                    '<td class="text-center">' + (data.eq_sn || '') + '</td>' +
                    '<td>' + (data.problem_text || '') + '</td>' +
                    '<td>' + (data.service_type == 'by_vendor' ? 'บริษัทภายนอก' : 'ทีมช่าง') + '</td>' +
                    '<td>' + (data.service_type=='by_vendor' ? data.sup_name : data.login) + '</td>' +
                    '<td class="text-right">' + numberWithCommas(data.amount_total, 2) + '</td>' +
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
