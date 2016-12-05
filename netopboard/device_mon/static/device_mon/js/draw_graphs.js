var highchartDefaultColors = ['#DB4D6D', '#66BAB7', '#f7a35c', '#8085e9',
   '#f15c80', '#ffd700', '#ffb6c1', '#32cd32', '#91e8e1', '#434348'];
Highcharts.setOptions({
    global: {
        useUTC: false
    }
});


function convert_bps(plain_bps){
  var short_bps=plain_bps;
  if(plain_bps >= Math.pow(10,9)){
    short_bps = String(plain_bps/Math.pow(10,9)).slice(0,5) + 'G';
  }else if(plain_bps >= Math.pow(10,6)){
    short_bps = String(plain_bps/Math.pow(10,6)).slice(0,5) + 'M';
  }else if(plain_bps >= Math.pow(10,3)){
    short_bps = String(plain_bps/Math.pow(10,3)).slice(0,5) + 'k';
  }
  short_bps = short_bps + 'bps';
  return short_bps;
}


var cpuChart = function(target, initial_data){
    chart = new Highcharts.Chart({
        chart: {
            renderTo: target,
            zoomType: 'xy',
            height: 240,
            spacing: [31, 3, 30, 0]
        },
        credits: {
          enabled: false
        },
        title: {
            text: '',
            floating: true,
            style: {
              fontSize: '24px'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                week: '%Y/%m/%d',
                month: '%Y/%m',
                year: '%Y'
            },
            labels: {step: 1, y: 30, rotation: -0,
              style: {
                fontSize: '12px'
              }
            },
        },
        yAxis: {
            title: {
                text: 'cpu use(%)'
            },
            opposite: true,
            min: 0,
            labels: {
              style: {
                fontSize: '12px'
              }
            }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%H:%M', this.x) +': '+ this.y + '%';
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 20,
            y: 0,
            borderWidth: 1,
            floating: true,
            backgroundColor: '#FFFFFF',
            itemStyle: {
              fontSize: '12px'
            }
        },
        plotOptions: {
            line: {
                marker: { enabled: false }
            },
            area: {
                marker: { enabled: false }
            }
        },
        colors: [
            '#FF4500'
        ],
        series: [
          {
            name: 'cpu_use',
            type: 'area',
            data: (function() {
              var data = [], time = (new Date()).getTime(), i;
              for (i = -59; i <= 0; i++) {
                data.push({x: time + i * 10000, y: 0});
              }
              return data;
            })()
          }
        ]
    });
    return chart;
};

var memoryChart = function(target, initial_data){
    chart = new Highcharts.Chart({
        chart: {
            renderTo: target,
            zoomType: 'xy',
            height: 240,
            spacing: [31, 3, 30, 0]
        },
        credits: {
          enabled: false
        },
        title: {
            text: '',
            floating: true,
            style: {
              fontSize: '24px'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                week: '%Y/%m/%d',
                month: '%Y/%m',
                year: '%Y'
            },
            labels: {step: 1, y: 30, rotation: -0,
              style: {
                fontSize: '12px'
              }
            },
        },
        yAxis: {
            title: {
                text: 'memory use(%)'
            },
            opposite: true,
            min: 0,
            labels: {
              style: {
                fontSize: '12px'
              }
            }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%H:%M', this.x) +': '+ this.y + '%';
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 20,
            y: 0,
            borderWidth: 1,
            floating: true,
            backgroundColor: '#FFFFFF',
            itemStyle: {
              fontSize: '12px'
            }
        },
        plotOptions: {
            line: {
                marker: { enabled: false }
            },
            area: {
                marker: { enabled: false }
            }
        },
        colors: [
            '#00AA90'
        ],
        series: [
          {
            name: 'memory_use',
            type: 'area',
            data: (function() {
              var data = [], time = (new Date()).getTime(), i;
              for (i = -59; i <= 0; i++) {
                data.push({x: time + i * 10000, y: 0});
              }
              return data;
            })()
          }
        ]
    });
    return chart;
};

var trafficChart = function(target, initial_data){
    chart = new Highcharts.Chart({
        chart: {
            renderTo: target,
            zoomType: 'xy',
            height: 240,
            spacing: [31, 3, 30, 0]
        },
        credits: {
          enabled: false
        },
        title: {
            text: '',
            floating: true,
            style: {
              fontSize: '24px'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: { // don't display the dummy year
                week: '%Y/%m/%d',
                month: '%Y/%m',
                year: '%Y'
            },
            labels: {step: 1, y: 30, rotation: -0,
              style: {
                fontSize: '12px'
              }
            },
        },
        yAxis: {
            title: {
                text: 'bps'
            },
            opposite: true,
            min: 0,
            labels: {
              style: {
                fontSize: '12px'
              }
            }
        },
        tooltip: {
            formatter: function() {
                    return '<b>'+ this.series.name +'</b><br/>'+
                    Highcharts.dateFormat('%H:%M', this.x) +': '+ convert_bps(this.y);
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 20,
            y: 0,
            borderWidth: 1,
            floating: true,
            backgroundColor: '#FFFFFF',
            itemStyle: {
              fontSize: '12px'
            }
        },
        plotOptions: {
            line: {
                marker: { enabled: false }
            },
            area: {
                marker: { enabled: false }
            }
        },
        colors: [
            '#B28FCE',
            '#58B2DC'
        ],
        series: [
          {
            name: 'in',
            type: 'area',
            data: (function() {
              var data = [], time = (new Date()).getTime() , i;
              for (i = -59; i <= 0; i++) {
                data.push({x: time + i * 10000, y: 0});
              }
              return data;
            })()
          }
          ,
          {
            name: 'out',
            type: 'line',
            data: (function() {
              var data = [], time = (new Date()).getTime() , i;
              for (i = -59; i <= 0; i++) {
                data.push({x: time + i * 10000, y: 0});
              }
              return data;
            })()
          }

        ]
    });
    return chart;
};
