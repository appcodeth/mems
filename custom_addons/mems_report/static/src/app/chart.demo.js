function numberWithCommas(num) {
  if(!num) {
    return;
  }
  return num.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function numberWithCommasDigits(num, digits) {
  if(!num) {
    return;
  }
  return num.toFixed(digits).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// TODO: Hard Code
company_id = 1

$(function () {
  var today = new Date();
  var currentDate = today.getDate() + '/' + (today.getMonth() + 1) + '/' + today.getFullYear();
  $('#currentDate').html(currentDate);

  $.ajax({
    url: '/api/dashboard/all?company_id=' + company_id,
    type: 'get',
    success: function (res) {
      if (res.ok) {
        $('#dash_sale_amount').html(numberWithCommas(res.sale_amount));
        $('#dash_count_bill').html(res.count_bill);
        $('#dash_average_bill').html(numberWithCommas((res.sale_amount / res.count_bill) || 0));
        $('#dash_grow_rate').html(numberWithCommasDigits(res.grow_rate, 1) + '%');
      }
    },
    error: function (err) {
      console.log('Connect error!', err)
    }
  });

  renderLineChart();
  renderBarChart();
  renderPieChart();
});

function renderLineChart() {
  var ctx = document.getElementById('lineCanvas').getContext('2d');
  $.ajax({
    url: '/api/dashboard/hours?company_id=' + company_id,
    type: 'get',
    success: function (res) {
      var lineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: res.labels,
          datasets: [{
            label: "ยอดขาย",
            fill: false,
            data: res.data,
            borderColor: 'rgba(60, 141, 188, 0.9)',
            backgroundColor: 'rgba(60, 141, 188, 0.9)',
          }]
        },
      });
    },
    error: function (err) {
      console.log('Connect error!', err)
    }
  });
}

function renderBarChart() {
  var ctx = document.getElementById('myChart').getContext('2d');

  $.ajax({
    url: '/api/dashboard/category?company_id=' + company_id,
    type: 'get',
    success: function (res) {
      var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: res.labels,
          datasets: [{
            label: 'ยอดขาย',
            data: res.data,
            backgroundColor: 'rgba(60, 141, 188, 0.9)',
            borderWidth: 1,
          }]
        },
        options: {
          plugins: {
            labels: false
          }
        }
      });
    },
    error: function (err) {
      console.log('Connect error!', err)
    }
  });


}

function renderPieChart() {
  var ctx = document.getElementById("pieCanvas").getContext('2d');

  $.ajax({
    url: '/api/dashboard/payment?company_id=' + company_id,
    type: 'get',
    success: function (res) {
      var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: res.labels,
          datasets: [{
            data: res.data,
            backgroundColor: [
              '#3c8dbc',
              '#f39c12',
              '#f56954',
              '#00a65a',
            ],
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutoutPercentage: 80,
          tooltips: {
            callbacks: {
              label: function (tooltipItem, data) {
                return data['labels'][tooltipItem['index']] + ': ' + data['datasets'][0]['data'][tooltipItem['index']] + '%';
              }
            }
          }
        }
      });
    },
    error: function (err) {
      console.log('Connect error!', err)
    }
  });


}
