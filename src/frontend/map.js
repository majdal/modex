$(function() {
 //todo: move this to a jquery oninit() handler
var labels =  new ol.style.Text({
        color: '#bada55',
        text: 'hello', //grrrrr. this doesn't work.
        fontFamily: 'Calibri,sans-serif',
        fontSize: 14
      })

var styleArray = [new ol.style.Style({
  //fill: new ol.style.Fill({
  //  color: 'rgba(255, 255, 255, 0.6)'
  //}),
  //symbolizers: [labels],
  stroke: new ol.style.Stroke({
    color: '#319FD3',
    width: 1
  })
})];

var pointStyle = [new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3,
      fill: new ol.style.Fill({color: 'red'}),
      stroke: new ol.style.Stroke({color: '#222222', width: 1.5})
    }),

  fill: new ol.style.Fill({
    color: 'rgba(255, 22, 255, 0.6)'
  }),
  stroke: new ol.style.Stroke({
    color: 'yellow',
    width: 2
  })


  })]

var styleArray2 = [new ol.style.Style({
  //image: new ol.style.Circle({
  fill: new ol.style.Fill({
    color: 'rgba(255, 22, 255, 0.6)'
  }),
  stroke: new ol.style.Stroke({
    color: 'yellow',
    width: 2
  })
  //})

})
];

styleArray2 = pointStyle;




var countries = new ol.layer.Vector({
  source: new ol.source.GeoJSON({
    url: 'assets/maps/countries.geojson'
  }),
  
  styleFunction: function(feature, resolution) {
    return styleArray;
  }
});

var meat = new ol.layer.Vector({
  source: new ol.source.GeoJSON({
    url: 'assets/maps/meatplants.geojson'
  }),
  styleFunction: function(feature, resolution) {
    return styleArray2;
  }

});


//          new ol.layer.Tile({     opacity: .5,        source: new ol.source.OSM()          }), //partially transparent

      var map = new ol.Map({
        renderer: ol.RendererHint.CANVAS, //the vector layer crashes without this. Go figure.
        target: 'map',
        layers: [
          new ol.layer.Tile({ source: new ol.source.MapQuest({layer: 'osm'}) }),
          countries,
          meat
        ],
        view: new ol.View2D({
          center: ol.proj.transform([-80.5, 43.45], 'EPSG:4326', 'EPSG:3857'), //these coordinates are not what you'll find on Wikipedia or in the World Fact Book. The Wikipedia coordinates, 43,28,0 N by 80,30,0W are A) in Degrees-Minutes-Seconds B) in WGS84 (so even once converted to decimal degrees they're slightly off)
          zoom: 11
        })
      });


}) //end oninit
