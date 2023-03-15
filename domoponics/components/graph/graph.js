function createGraph(id,data,label, color, labels){
    var config = {
        type: 'line',
        data: {
        datasets: [{
            data: data,
            label: label,
            fill: false,
        
            borderColor: color,
            backgroundColor: color,
            pointStyle: 'rectRounded',
            pointRadius: 10,
            pointHoverRadius: 15}],
            labels: labels
        },
        options: {
        responsive: true,
        scales: {
                    xAxes: [{
                        type: "time",
                        time: {
                            unit: "minute",
                            displayFormats: {
                                month: "MMM yyyy"
                            }
                        },
                        scaleLabel: {
                            display: true,
                            labelString: "Date"
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: label
                        }
                    }]
                }
        }
    };

    var ctx = document.getElementById('graph-sensor-'+id).getContext('2d');
    window.myPie = new Chart(ctx, config);
}

