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
        url: '/api/inventory/move',
        type: 'get',
        async: false,
        success: function (res) {
            var temp_code = '';

            var total_qty = 0;

            $.each(res.rows, function (index, data) {
                var sep = '';
                if(temp_code != data.code) {
                    sep = '<tr style="color:#369"><td colspan="20"><strong>[' + data.code + '] ' + data.name + ' // คงเหลือ: ' + numberWithCommas(data.stock_qty, 0) + ' ' + (data.uom_name || '') + '</strong></td></tr>';
                    temp_code = data.code;
                }

                if(data.doc_type == 'init') {
                    total_qty = data.int_qty;
                }
                if(data.doc_type == 'adjust') {
                    total_qty = data.adjust_qty;
                }

                if(data.doc_type == 'receive' || data.doc_type == 'return') {
                    total_qty += data.int_qty;
                } else if(data.doc_type == 'issue') {
                    total_qty -= data.out_qty;
                }

                tr += sep + '<tr>' +
                    '<td class="text-center">' + data.move_date + '</td>' +
                    '<td>' + (data.doc_type_desc || '') + '</td>' +
                    '<td>' + (data.doc_name || '') + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.int_qty, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.out_qty, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(data.adjust_qty, 0) + '</td>' +
                    '<td class="text-center">' + numberWithCommas(total_qty, 0) + '</td>' +
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
