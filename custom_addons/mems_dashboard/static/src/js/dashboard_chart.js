function numberWithCommas(num) {
    if (!num)
        return 0;
    return num.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function numberWithCommas(num, digits) {
    if (!num)
        return 0;
    return num.toFixed(digits).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// counter report
function runReport() {
    $.ajax({
        url: '/api/dashboard/count',
        type: 'get',
        async: false,
        success: function (res) {
            $.each(res.rows, function (index, data) {
                $('#count-active').html(numberWithCommas(data.count_active,0));
                $('#count-repair').html(numberWithCommas(data.count_repair,0));
                $('#count-pm').html(numberWithCommas(data.count_pm,0));
                $('#count-pulling').html(numberWithCommas(data.count_pulling,0));
            });
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

// colors
window.chartColors = {
    red: 'rgba(221, 75, 57, 0.6)',
    orange: 'rgb(243, 156, 18, 0.6)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgba(0, 166, 90, 0.6)',
    blue: 'rgba(0, 192, 239, 0.6)',
    purple: 'rgba(153, 102, 255, 0.8)',
    grey: 'rgba(201, 203, 207, 0.8)',
};

Chart.defaults.global.defaultFontFamily = 'Kanit';

// bar chart
var ctx = document.getElementById('myChart').getContext('2d');
var chartData = {
    labels: ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'],
    datasets: [
        {
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            borderWidth: 1,
            label: 'ทั้งหมด',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
        {
            backgroundColor: window.chartColors.green,
            borderColor: window.chartColors.green,
            borderWidth: 1,
            label: 'ซ่อมเสร็จ',
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        },
    ]
};

var myBarChart = new Chart(ctx, {
    type: 'bar',
    options: {
        barValueSpacing: 20,
        plugins: {
            datalabels: {
                display: false
            },
            outlabels: {
                display: true
            }
        },
        scales: {
            yAxes: [{
                ticks: { min: 0 }
            }]
        }
    }
});

// pie chart
var pieChartData = {
    labels: ['ซ่อมโดยทีม', 'ซ่อมโดยบริษัท'],
    datasets: [{
        backgroundColor: ['#3e95cd', '#8e5ea2'],
        data: [0,0]
    }]
};

var myPieChart = new Chart(document.getElementById('pie-chart'), {
    type: 'pie',
    options: {
        legend: {
            display: false
        },
        title: {
            display: false,
        },
        plugins: {
            datalabels: {
                formatter: (value, ctx) => {
                    let sum = 0;
                    let dataArr = ctx.chart.data.datasets[0].data;
                    dataArr.map(data => {
                        sum += data;
                    });
                    let percentage = (value*100 / sum).toFixed(1)+'%';
                    return ctx.chart.data.labels[ctx.dataIndex] + '\n' + percentage;
                },
                color: '#fff',
            }
        }
    }
});

// main function of barChart
function runBarChart() {
    $.ajax({
        url: '/api/dashboard/barchart',
        type: 'get',
        async: false,
        success: function (res) {
            chartData.datasets[0].data = res.rows1;
            chartData.datasets[1].data = res.rows2;
            myBarChart.data = chartData;
            myBarChart.update();
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

// main function of pieChart
function runPieChart() {
    $.ajax({
        url: '/api/dashboard/piechart',
        type: 'get',
        async: false,
        success: function (res) {
            pieChartData.datasets[0].data = res.rows;
            myPieChart.data = pieChartData;
            myPieChart.update();
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

// link to workorder form
function gotoMenu(id) {
    $.get('/api/getmenu?model_id=mems.workorder&menu_name=Work Order', function (res) {
        if (res.menu_id) {
            window.location.href = '/web#view_type=form&model=mems.workorder&menu_id=' + res.menu_id + '&action=' + res.action_id + '&id=' + id;
        } else {
            alert('Can not link menu!!');
        }
    });
}

// get workorder list
var table_result = $('#table-workorder');
var beginHtml = table_result.html();

function runWorkOrderList() {
    table_result.html('');
    table_result.append(beginHtml);
    table_result.hide();

    var tr = '';
    $.ajax({
        url: '/api/dashboard/workorder',
        type: 'get',
        async: false,
        success: function (res) {
            $('#data-count').html('(' + res.rows.length + ')');
            $.each(res.rows, function (index, data) {
                tr += '<tr>' +
                    '<td><a href="javascript:gotoMenu(' + data.id + ')">' + (data.name || '') + '</a></td>' +
                    '<td>' + (data.wo_name || '') + '</td>' +
                    '<td style="color:#080">' + (data.state || '') + '</td>' +
                    '<td><a href="javascript:gotoMenu(' + data.id + ')" class="btn btn-default">เปิดดู</a></td>' +
                '</tr>';
            });
            table_result.append('<tbody>' + tr + '</tbody>');
            table_result.show();
        },
        error: function (err) {
            console.log('Connect error!', err);
        }
    });
}

// main
$(function () {
    runReport();
    runBarChart();
    runPieChart();
    runWorkOrderList();
});
