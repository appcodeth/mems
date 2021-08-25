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
        url: '/api/equipment/warranty',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                var status = '';
                if (data.no_day <= 30 && data.no_day > 0) {
                    status = 'ใกล้หมดประกัน (เหลือ '+ (data.no_day + 1) +' วัน)';
                } else if(data.no_day <= 0) {
                    status = 'หมดประกันแล้ว';
                }

                tr += '<tr>' +
                    '<td class="text-center">' + (data.code || '') + '</td>' +
                    '<td>' + (data.name || '') + '</td>' +
                    '<td>' + (data.categ_name || '') + '</td>' +
                    '<td>' + (data.uom_name || '') + '</td>' +
                    '<td>' + (data.brand_name + '/' + data.model_name) + '</td>' +
                    '<td>' + (data.serial_no || '') + '</td>' +
                    '<td class="text-center">' + (data.warranty_start_date || '') + '</td>' +
                    '<td class="text-center">' + (data.warranty_end_date || '') + '</td>' +
                    '<td>' + (data.sup_name || '') + '</td>' +
                    '<td>' + (status || '') + '</td>' +
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
