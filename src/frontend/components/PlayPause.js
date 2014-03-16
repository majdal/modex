Crafty.c('PlayPause', {
	isPaused: true, 

	init : function() {
		this.requires("2D, Canvas, Mouse, playButton");
		var positionY = Crafty.viewport.height-250;
		
		this.attr({x: 20, y: positionY, w: 100, h: 100})
		//.animate("press", [[20, 20]]).animate("release", [[0, 20]])
		 .bind("Click", function(){
			if (this.isPaused) {
				this.addComponent("pauseButton").removeComponent("playButton");
				this.isPaused = false;
				var game = this.serializeGame();
				ctl.send(game);
			}
			else {
				this.addComponent("playButton").removeComponent("pauseButton");
				this.isPaused = true;
			}
		})
	},

	serializeGame: function() {
		//Game.
	}
});