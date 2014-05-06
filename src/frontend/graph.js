/* graph.js
 *   draws a multi-timeseries linegraph from data passed over a websocket
 */


$(function() {
  // TODO move scope to the window.Game namespace 
  scope = {} //hacks
  scope.data = [] //makes a data array that is safely accessible from anywhere in this file; sidesteps any weird js scoping rules that might kick in if we tried to make data a (pseudo)global
  
  var parseDate = d3.time.format("%Y%m%d").parse;
    
  var margin = {top: 20, right: 80, bottom: 30, left: 50};
  
  //width = 960 - margin.left - margin.right,
  //height = 500 - margin.top - margin.bottom;
  width = $("#graph").width() - margin.left - margin.right;
  height = $("#graph").height() - margin.top - margin.bottom;
        
  var svg = d3.select("#graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")"
        );
  var chart;
  
  nv.addGraph(function() {
    chart = nv.models.lineChart()
    .options({ width: width,    //it is super awkward that we have to define these; isn't d3 supposed to just figure this out?
               height: height,  //it might even be doing that, but it seems (try clicking the nvd3 legends on and off and watch
                                //the inspector---it resets the <rect> width exactly when you click) nvd3 has other plans in mind
               margin: {top: 10, right: 10, bottom: 15, left: 10}, //all these pixel measurements are hurtful
                        
               showXAxis: true,
               showYAxis: true,
               showLegend: true,
    });
    
    chart.xAxis
      .axisLabel("Time")
      .tickFormat(d3.format(",1f"));

    chart.yAxis
      .axisLabel("Quantity")
      .tickFormat(d3.format(',.1f'));
      
    chart.x(function(d,i) { return d.x});   // use the .x value for x-axis location (rather than i)
    nv.utils.windowResize(chart.update); //what does this do? do we need this?

    return chart;
  });

//Game.dataSocket.onmessage
  var notused = function(d) {
    //console.log("received data from (plain) websocket:", d)
    d = JSON.parse(d.data);
    var time = d[0]
    var series = d[1]
    //d.date = parseDate(d.date);
    
    //loop through and format data into line graph data for nv
    for(key in series) {
      addData(key, time, [series[key]]);
    }      

    // update the chart with the data
    svg.datum(scope.data)
       .call(chart);
    //scope.data.push(d)
    //draw()
  };
    
  //add Data to pre-existing line
  function addData(keyval,xval,yval) {
    var notthere = true
    //if there is already a line for the data add it to that line
    for(var i = 0; i < scope.data.length; i++) { // FIXME: switch to $.each() or $.map(). Looping over an array this way has caused me headaches in the past. 
      if(scope.data[i].key == keyval) {
        notthere = false;
        scope.data[i].values.push({x:xval, y:yval});
      }
    }
    
    //otherwise add a new line
    if(notthere){
      var new_line = {values: [{x:xval, y:yval}],
                      key: keyval,
                      color: getRandomColor()
                  }
      scope.data.push(new_line);
    }
  };
  
  // Just to be pretty
  function getRandomColor() {
    // some colour pairs appropriate for the colour blind, as shown by http://colorschemedesigner.com/:
    // rgb(42,23,177) vs rgb(255,201,0)
    //   (blueish)         (yellowish)
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
      color += letters[Math.round(Math.random() * 15)];
    }
    return color;
  };
   
})
