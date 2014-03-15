/* graph.js
 *   draws a multi-timeseries linegraph from data passed over a websocket
 */


$(function() {

   scope = {} //hacks
   scope.data = [] //makes a data array that is safely accessible from anywhere in this file; sidesteps any weird js scoping rules that might kick in if we tried to make data a (pseudo)global
   
   var parseDate = d3.time.format("%Y%m%d").parse;
    
    var margin = {top: 20, right: 80, bottom: 30, left: 50},
    
    //width = 960 - margin.left - margin.right,
    //height = 500 - margin.top - margin.bottom;
    width = $("#graph").width() - margin.left - margin.right
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
		.options({
			margin: {top: 20, right: 350, bottom: 30, left: 50},
			showXAxis: true,
			showYAxis: true,
			showLegend: true,
		})
		;
		
		chart.xAxis
			.axisLabel("Time")
			.tickFormat(function(d) { return d3.time.format('%b %d, %Y')(new Date(d)) })
			;
		chart.yAxis
			.axisLabel("Quantity")
			.tickFormat(d3.format(',.1f'))
			;
			
		chart.x(function(d,i) { return d.x}); 	// use the .x value for x-axis 
                                           		//  location (rather than i)
                     
        
        nv.utils.windowResize(chart.update);

  		return chart;
	})
    
    
    
    data_socket = new WebSocket("ws://" + location.host + "/ws") //our websocket sits at /ws (TODO(kousu): reorg this)
    data_socket.onmessage = function(d) {
      //console.log("received data from (plain) websocket:", d)
      d = JSON.parse(d.data);
      var time = d[0]
      var series = d[1]
      //d.date = parseDate(d.date);
      
      //loop through and format data into line graph data for nv
      for(key in series) {
        console.log("adding", time, [series[key]])
	addData(key, time, [series[key]]);
      }      
      
      svg // update the chart with the data
        .datum(scope.data)
        .call(chart);
      //console.log(d);
      //scope.data.push(d)
      //draw()
    }
    
    //add Data to pre-existing line
    function addData(keyval,xval,yval){
    	var notthere = true
    	//if there is already a line for the data add it to that line
    	for(var i = 0; i < scope.data.length; i++){
    		if(scope.data[i].key == keyval){
    			notthere = false;
    			scope.data[i].values.push({x:xval, y:yval});
    		}
    	}
    	
    	//otherwise add a new line
    	if(notthere){
    		var new_line = {
    		values: [{x:xval, y:yval}],
    		key: keyval,
    		color: getRandomColor()
    		}
    		scope.data.push(new_line);
    	}
    		
    }
    
    // Just to be pretty
	function getRandomColor() {
		var letters = '0123456789ABCDEF'.split('');
		var color = '#';
		for (var i = 0; i < 6; i++ ) {
			color += letters[Math.round(Math.random() * 15)];
		}
		return color;
	}
   
  })
