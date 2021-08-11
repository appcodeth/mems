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

function twoDigitsNumber(num) {
    if (!num)
        return;
    if (num < 10) {
        return '0' + num;
    }
    return num;
}

function getDate(s) {
    var temps = s.split('/');
    return temps[2] + '-' + temps[1] + '-' + temps[0];
}

function getLastDay(y, m) {
    return new Date(y, m + 1, 0).getDate();
}
