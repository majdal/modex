Crafty.scene('game', function() {
  // clear the background so we can see the map
  Crafty.background('url(assets/images/FFFFFF-0.png)');

  // The layers
  var watercolor = new ol.layer.Tile({
         source: new ol.source.Stamen({
           layer: 'watercolor'
         })
       });

  // lables layer, currently not used
  var lables = new ol.layer.Tile({
         source: new ol.source.Stamen({
           layer: 'terrain-labels'
         })
       });

  // draw the map
  var map = new ol.Map({
    target: 'map',
    layers: [watercolor,],
    view: new ol.View2D({
      center: ol.proj.transform([-80.5, 43.45], 'EPSG:4326', 'EPSG:3857'), //these coordinates are not what you'll find on Wikipedia or in the World Fact Book. The Wikipedia coordinates, 43,28,0 N by 80,30,0W are A) in Degrees-Minutes-Seconds B) in WGS84 (so even once converted to decimal degrees they're slightly off)
      zoom: 7
    }) 
  });


  plusButton = Crafty.e('AddScenario');

  pauseButton = Crafty.e('PlayPause');

});
