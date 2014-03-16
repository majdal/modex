Crafty.c('PlayPause', {
    isPaused: true, 

    init : function() {
        this.requires("2D, Canvas, Mouse, playButton");
        var positionY = Crafty.viewport.height-200;
        
        this.attr({x: 20, y: positionY, w: 100, h: 100})
         .bind("Click", function(){
            if (this.isPaused) {
                this.addComponent("pauseButton").removeComponent("playButton");
                this.isPaused = false;
                var game = plusButton.serialize();
                game = JSON.stringify(game);
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