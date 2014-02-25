$(document).ready(function() {

    ws = new WebSocket("ws://" + location.host + "/ws") //our websocket sits at /ws (TODO(kousu): reorg this)
    ws.onopen = function() { 
       this.send(""); //poke the server to get data out
    }
    ws.onmessage = function(d) {
      d = JSON.parse(d.data);
      //console.log("received data from websocket:")
      console.log(d);
    }

    var svg = dimple.newSvg("#graph", 590, 400);
    d3.tsv("/assets/data/example_data.tsv", function (data) {
      data = dimple.filterData(data, "Owner", ["Aperture", "Black Mesa"])
      var myChart = new dimple.chart(svg, data);
      myChart.setBounds(60, 30, 505, 305);
      var x = myChart.addCategoryAxis("x", "Month");
      x.addOrderRule("Date");
      myChart.addMeasureAxis("y", "Unit Sales");
      myChart.addSeries("Channel", dimple.plot.line);
      myChart.addLegend(60, 10, 500, 20, "right");
      myChart.draw();
    });
    //chart.draw();
    /*   

    function d3Chart(id, data, width, height, padding) {
            this.id = id
            this.data = data
            this.width = width
            this.height = height
            this.padding = padding
            this.svg = function(){ 
                var element = d3.select("#graph")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "chart")
                .attr("id", id);
            this.yscale = d3.scale.linear()
                .domain([0, d3.max(data)])
                .range([height - padding, padding])
            this.xscale = d3.scale.ordinal()
                .domain(d3.range(data.length))
                .rangeRoundBands([padding,width-padding], 0.05)
            return element
            }
            this.element = this.svg()

            this.rect = function() {

            this.rect = this.element.selectAll("rect")
                .data(this.data)
                .enter()
                .append("rect");
                }
            this.plot = function() {
                var self = this;
                this.rect.attr("x", function(d, i, self) {
                        return self.xscale(i);
                    })
                    .attr("y", function (d, self) {
                        return self.yscale(d);
                    })
                    .attr("width", this.xscale.rangeBand())
                    .attr("height", function(d) {
                        return this.height - this.padding - this.yscale(d);
                    })
                    .attr("fill", function(d) {
                        return "rgb(" + (100 - d) + ", 0, " + (d*10) + ")";
                    });
            }

        };

        var data = [3, 6, 2, 7, 5, 2, 0, 3, 8, 9, 2, 5, 9, 3, 6, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 2, 7];

        var chart = new d3Chart("yearly", [1, 2, 3, 4, 5, 6, 7, 8, 9], 600, 400, 40);
        chart.rect()
        chart.plot()
 

         d3Chart.prototype.rect = function() {

            this.rect = this.svg.selectAll("rect")
                .data(this.data)
                .enter()
                .append("rect");
        }

        d3Chart.prototype.plot = function() {
            var self = this;
            this.rect.attr("x", function(d, i, self) {
                    return self.xscale(i);
                })
                .attr("y", function (d, self) {
                    return self.yscale(d);
                })
                .attr("width", this.xscale.rangeBand())
                .attr("height", function(d) {
                    return this.height - this.padding - this.yscale(d);
                })
                .attr("fill", function(d) {
                    return "rgb(" + (100 - d) + ", 0, " + (d*10) + ")";
                });
            }


    function defaultFor(arg, val) { return typeof arg !== 'undefined' ? arg : val; }

    function plot(numberOfYears) {
      this.numberOfYears = defaultFor(numberOfYears, 10);
      this.dimensions = {width: window.width - 200, height: window.height * 0.1};
      this.margin = {top: 20, right: 80, bottom: 30, left: 50};
      this.svg = d3.select("#graph").append("svg")
          .attr("width", this.dimensions.width)
          .attr("height", this.dimensions.height)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    }



    var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y%m%d").parse;

    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var color = d3.scale.category10();

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var line = d3.svg.line()
        .interpolate("basis")
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.temperature); });

    var svg = d3.select("#graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.tsv("assets/data/static_lightbulbs.tsv", function(error, data) {
      color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

      data.forEach(function(d) {
        d.date = parseDate(d.date);
      });

      var cities = color.domain().map(function(name) {
        return {
          name: name,
          values: data.map(function(d) {
            return {date: d.date, temperature: +d[name]};
          })
        };
      });

      x.domain(d3.extent(data, function(d) { return d.date; }));

      y.domain([
        d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
        d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
      ]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Temperature (ºF)");

      var city = svg.selectAll(".city")
          .data(cities)
        .enter().append("g")
          .attr("class", "city");

      city.append("path")
          .attr("class", "line")
          .attr("d", function(d) { return line(d.values); })
          .style("stroke", function(d) { return color(d.name); });

      city.append("text")
          .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
          .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
          .attr("x", 3)
          .attr("dy", ".35em")
          .text(function(d) { return d.name; });
      });
    //$('#cr-stage').hide();
    */
});
