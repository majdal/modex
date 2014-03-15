/**@
* #PlayPause
* @category Custom
*
* A simple play/pause button for the game
*
*/

/*
Crafty.c("PlayPause", {
	init: function(entity) {
		this.requires("2D");
		this._pbFilledFraction = 0;
	},

	play: function() {
		console.log('play');
	},

	pause: function() {
		console.log('pause');
	},
});*/

Crafty.c('PlayPause', {
	isPaused: true, 

	init : function(){
		this.requires("2D, Canvas, Mouse, playButton");
		var positionY = Crafty.viewport.height-250;
		
		this.attr({x: 20, y: positionY, w: 100, h: 100})
		//.animate("press", [[20, 20]]).animate("release", [[0, 20]])
		 .bind("Click", function(){
			if (this.isPaused) {
				this.addComponent("pauseButton").removeComponent("playButton");
				this.isPaused = false;
			}
			else {
				this.addComponent("playButton").removeComponent("pauseButton");
				this.isPaused = true;
			}
		}) 
		
		/*.animate("press", [[20, 20]]).animate("release", [[0, 20]])
		.bind('Click', function(){
        buttonAnimate(button.PAUSE, "press");
    	})
        .bind('Click', function() { 
        buttonAnimate(button.PAUSE, "release");
    	})

    	var buttonAnimate = function(btn, action){
    		var pauseplay

    		switch (btn){
    			case button.PAUSE:
    			pauseplay = pauseButton;
    			break;
    		}

    		pauseplay.animate(action, 1, 0);
    	}*/
	},
});