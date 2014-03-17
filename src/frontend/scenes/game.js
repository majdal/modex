Crafty.scene('game', function() {
  // clear the background so we can see the map
  Crafty.background('url(assets/images/FFFFFF-0.png)');

  // The layers
  var watercolor = new ol.layer.Tile({
         source: new ol.source.Stamen({
           layer: 'watercolor'
         })
       });

  // labels layer, currently not used
  var labels = new ol.layer.Tile({
         source: new ol.source.Stamen({
           layer: 'terrain-labels'
         })
       });

  var farms = new ol.layer.Vector({
    source: new ol.source.TopoJSON({ url: '/assets/maps/elora.topo.json'  } ), 
    styleFunction: function(feature, resolution) {
      return [new ol.style.Style({ fill: new ol.style.Fill({ color: 'hsla(100, 50%,30%, .5)'}),  //TODO: look at feature and colour accordingly; for example: change hue by wealth and alpha by activity or something
                                   stroke: new ol.style.Stroke({ color: 'hsla(290, 50%, 50%, .3)', width: 2 })  
                          })
      ];
    } //styleFunction
  });

  // draw the map
  var map = new ol.Map({
    renderer: ol.RendererHint.CANVAS, //the vector layer crashes without this
    target: 'map',
    layers: [watercolor, farms],
    view: new ol.View2D({
      center: ol.proj.transform([-80.56, 43.65], 'EPSG:4326', 'EPSG:3857'), //these coordinates are not what you'll find on Wikipedia or in the World Fact Book. The Wikipedia coordinates, 43,28,0 N by 80,30,0W are A) in Degrees-Minutes-Seconds B) in WGS84 (so even once converted to decimal degrees they're slightly off)
      zoom: 12
    }) 
  });

  plusButton = Crafty.e('AddScenario');
  // add an initial scenario and select it
  plusButton.addScenario();

  playButton = Crafty.e('PlayPause');

  //back button to Menu screen

  Crafty.e("2D, DOM, backButton, Mouse").attr({
      x: 0,
      y: 0
   }).bind('Click', function() {
      Crafty.scene("menu");
    });
/*
  redSquare = Crafty.e('2D, Canvas, Color, Mouse')
                     .attr({x: 100, y: 600, w: 100, h: 100})
                     .color('red')
                     .bind('Click', function() {
                       var data = plusButton.serialize();
                       ctl.send()
                     });
*/
});
