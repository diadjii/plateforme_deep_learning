var ctx = document.getElementById('myChart').getContext('2d');
var data_core1 = [], data_core2 = [], data_core3 = [], data_core4 = [], labels = [], freqs = [], temp = [];

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Frequences (Mhz)',
            data: freqs,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false
        }
        ]
    },
    options: {
        legend: {
            position: 'top',
            labels: {
                fontColor: 'black'
            }
        },
    }
});

let options = {
    legend: {
        position: 'top',
        labels: {
            fontColor: 'black'
        }
    },
}



var i = 0;

var ctxCore1 = document.getElementById('core1').getContext('2d');
var myChartCore1 = new Chart(ctxCore1, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Core 1',
            data: data_core1,
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false
        },
        ]
    },
    options: options
});

var ctxCore2 = document.getElementById('core2').getContext('2d');
var myChartCore2 = new Chart(ctxCore2, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Core 2',
            data: data_core2,
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: false
        },
        ]
    },
    options: options
});

var ctxCore3 = document.getElementById('core3').getContext('2d');
var myChartCore3 = new Chart(ctxCore3, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Core 3',
            data: data_core3,
            borderColor: 'rgba(255, 206, 86, 1)',
            borderWidth: 1,
            fill: false
        },
        ]
    },
    options: options
});

var ctxCore4 = document.getElementById('core4').getContext('2d');
var myChartCore4 = new Chart(ctxCore4, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Core 4',
            data: data_core4,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            fill: false
        },
        ]
    },
    options: options
});


setInterval(function () {
    $.get("/state").done(response => {
        console.log(response)
        $("#ram").text("Ram : "+response.ram_usage)
        updateFreqsAndTemp(response.current_freq, response.temperature.asus[0][1]);
        updateCore1(response.Core_0)
        updateCore2(response.Core_1)
        updateCore3(response.Core_2)
        updateCore4(response.Core_3)
        if (i > 30) {
            data_core1.shift()
            data_core2.shift()
            data_core3.shift()
            data_core4.shift()
            freqs.shift();
        } else {
            labels.push((i++));
        }

    }).fail(error => {
        console.log("error")
    })
}, 2000);

function updateFreqsAndTemp(freqVal, tempVal) {
    $("#core1_val").text(freqVal + "%");
    $("#temp").text("Température : "+tempVal + "°C");
    freqs.push(freqVal);
    myChart.update();
}

function updateCore1(core1Val) {
    $("#core1_val").text(core1Val + "%");
    data_core1.push(core1Val);
    myChartCore1.update();
}

function updateCore2(core2Val) {
    $("#core2_val").text(core2Val + "%");
    data_core2.push(core2Val);
    myChartCore2.update();
}

function updateCore3(core3Val) {
    $("#core3_val").text(core3Val + "%");
    data_core3.push(core3Val);
    myChartCore3.update();
}

function updateCore4(core4Val) {
    $("#core4_val").text(core4Val + "%");
    data_core4.push(core4Val);
    myChartCore4.update();
}

