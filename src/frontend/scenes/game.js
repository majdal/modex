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
      //center: ol.proj.transform([-122.416667, 37.783333], 'EPSG:4326', 'EPSG:3857'),
      zoom: 7
    }) 
  });
  //$('#map').show();

  Crafty.e('2D, DOM, Text')
    .attr({ x: 100, y: 190 })
    .text('Victory!');

  this.restart_game = this.bind('KeyDown', function() {
      Crafty.scene('game');
    });
  }, function() {
    this.unbind('KeyDown', this.restart_game);
});

/* 

Crafty.scene('game', function() {

  // A 2D array to keep track of all occupied tiles
  this.occupied = new Array(Game.map_grid.width);
  for (var i = 0; i < Game.map_grid.width; i++) {
    this.occupied[i] = new Array(Game.map_grid.height);
    for (var y = 0; y < Game.map_grid.height; y++) {
      this.occupied[i][y] = false;
    }
  }

  // Player character, placed at 5, 5 on our grid
  this.player = Crafty.e('PlayerCharacter').at(5, 5);
  this.occupied[this.player.at().x][this.player.at().y] = true;

  // Place a tree at every edge square on our grid of 16x16 tiles
  for (var x = 0; x < Game.map_grid.width; x++) {
    for (var y = 0; y < Game.map_grid.height; y++) {
      var at_edge = x == 0 || x == Game.map_grid.width - 1 || y == 0 || y == Game.map_grid.height - 1;

      if (at_edge) {
        // Place a tree entity at the current tile
        Crafty.e('Tree').at(x, y);
        this.occupied[x][y] = true;
      } else if (Math.random() < 0.06 && !this.occupied[x][y]) {
        // Place a bush entity at the current tile
        Crafty.e('Bush').at(x, y);
        this.occupied[x][y] = true;
      }
    }
  }

  // Generate up to five villages on the map in random locations
  var max_villages = 5;
  for (var x = 0; x < Game.map_grid.width; x++) {
    for (var y = 0; y < Game.map_grid.height; y++) {
      if (Math.random() < 0.02) {
        if (Crafty('Village').length < max_villages && !this.occupied[x][y]) {
          Crafty.e('Village').at(x, y);
        }
      }
    }
  }

  this.show_victory = this.bind('VillageVisited', function() {
    if (!Crafty('Village').length) {
      Crafty.scene('Victory');
    }
  });
}, function() {
  this.unbind('VillageVisited', this.show_victory);
});
*/