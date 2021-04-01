var myConfig = {
  type: "gauge",
  scale: {
    sizeFactor: 2.5
  },
  backgroundColor: "rgba(0,0,0,0)",
  globals: {
    fontSize: 15
  },
  plotarea: {
    marginTop: 65
  },
  plot: {
    // fontcolor: "black",
    size: '100%',
    valueBox: {
      placement: 'center',
      text: '%v', //default
      fontSize: 13,
      rules: [{
          rule: '%v >= 8',
          text: '%v kg<br>Very High'
        },
        {
          rule: '%v < 8 && %v > 6',
          text: '%v kg<br>High'
        },
        {
          rule: '%v < 6 && %v > 4',
          text: '% kg<br>Average'
        },
        {
          rule: '%v < 4 && %v > 2',
          text: '%v kg<br>Low'
        },
        {
          rule: '%v <  2',
          text: '%v kg<br>Very Low'
        }
      ]
    }
  },
  tooltip: {
    borderRadius: 0
  },
  scaleR: {
    aperture: 200,
    values: "0:10:2",
    center: {
      visible: false
    },
    tick: {
      visible: false
    },
    item: {
      offsetR: 0,
      rules: [{
        rule: '%i == 9',
        offsetX: 15
      }]
    },
    ring: {
      size: 10,
      rules: [{
        "rule": "%v >= 0 && %v <= 2",
        "background-color": "green"
      },
      {
        "rule": "%v >= 2 && %v <= 4",
        "background-color": "Chartreuse"
      },
      {
        "rule": "%v >= 4 && %v <= 6",
        "background-color": "yellow"
      },
      {
        "rule": "%v >= 6 && %v <= 8",
        "background-color": "orange"
      },
      {
        "rule": "%v >= 8 && %v <=10",
        "background-color": "red"
      }
      ]
    }
  },
  refresh: {
    type: "feed",
    transport: "js",
    url: "feed()",
    interval: 1500,
    resetTimeout: 1000
  },
  series: [{
    values: [],
    backgroundColor: 'black',
    indicator: [5, 5, 5, 5, 0.75],
    animation: {
      effect: 2,
      method: 1,
      sequence: 4,
      speed: 900
    },
  }]
};

var NL_gauge_Config = {
  type: "gauge",
  scale: {
    sizeFactor: 2.5
  },
  backgroundColor: "rgba(0,0,0,0)",
  globals: {
    fontSize: 15
  },
  plotarea: {
    marginTop: 65
  },
  plot: {
    // fontcolor: "black",
    size: '100%',
    valueBox: {
      placement: 'center',
      text: '%v', //default
      fontSize: 13,
      rules: [{
          rule: '%v >= 8',
          text: '%v kg<br>Very High'
        },
        {
          rule: '%v < 8 && %v > 6',
          text: '%v kg<br>High'
        },
        {
          rule: '%v < 6 && %v > 4',
          text: '%v kg<br>Average'
        },
        {
          rule: '%v < 4 && %v > 2',
          text: '%v kg<br>Low'
        },
        {
          rule: '%v <  2',
          text: '%v kg<br>Very Low'
        }
      ]
    }
  },
  tooltip: {
    borderRadius: 5
  },
  scaleR: {
    aperture: 200,
    values: "0:10:2",
    center: {
      visible: false
    },
    tick: {
      visible: false
    },
    item: {
      offsetR: 0,
      rules: [{
        rule: '%i == 9',
        offsetX: 15
      }]
    },
    ring: {
      size: 10,
      rules: [{
        "rule": "%v >= 0 && %v <= 2",
        "background-color": "green"
      },
      {
        "rule": "%v >= 2 && %v <= 4",
        "background-color": "Chartreuse"
      },
      {
        "rule": "%v >= 4 && %v <= 6",
        "background-color": "yellow"
      },
      {
        "rule": "%v >= 6 && %v <= 8",
        "background-color": "orange"
      },
      {
        "rule": "%v >= 8 && %v <=10",
        "background-color": "red"
      }
      ]
    }
  },
  refresh: {
    type: "feed",
    transport: "js",
    url: "feed()",
    interval: 1500,
    resetTimeout: 1000
  },
  series: [{
    values: [],
    backgroundColor: 'black',
    indicator: [5, 5, 5, 5, 0.75],
    animation: {
      effect: 2,
      method: 1,
      sequence: 4,
      speed: 900
    },
  }]
};

function CalculateCo2() {
  var fetch_url = "/calculate";
  fetch(fetch_url)
    .then(response => response.json())
    .then(function(data) {
      if (data.co2_score == 0.0) {
        myConfig['series'][0]['values'] = [0.0];
        zingchart.render({
          id: 'myChart',
          data: myConfig,
          height: '100%',
          width: '100%'
      });  
      }
      else {
        // document.getElementById("co2-score").innerHTML = "Jouw co2 score is: " + data.co2_score.toFixed(2);
        myConfig['series'][0]['values'] = [Number(data.co2_score.toFixed(2))];
        zingchart.render({
          id: 'myChart',
          data: myConfig,
          height: '100%',
          width: '100%'
      });  
      }
      NL_gauge_Config['series'][0]['values'] = [5.4];
      zingchart.render({
        id: 'NL_gauge',
        data: NL_gauge_Config,
        height: '100%',
        width: '100%'
    });
  });
}