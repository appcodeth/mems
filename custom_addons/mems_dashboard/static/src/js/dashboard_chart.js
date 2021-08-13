var ctx = document.getElementById('myChart').getContext('2d');

var data = {
    labels: ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'],
    datasets: [
        {
            label: 'Target',
            data: [3, 7, 4, 5, 5, 2, 1, 3, 3, 3, 5, 6]
        },
        {
            label: 'Actual',
            data: [4, 3, 2, 3, 1, 3, 3, 6, 7, 8, 1, 1]
        },
    ]
};

var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: data,
    options: {
        barValueSpacing: 20,
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                }
            }]
        }
    }
});
