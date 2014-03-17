Crafty.c('PlayPause', {
    isPaused: true, 

    init : function() {
        this.requires("2D, Canvas, Mouse, playButton");
        var positionY = Crafty.viewport.height-200;
        
        this.attr({x: 20, y: positionY, w: 100, h: 100})
            .bind("Click", function(){
                if (this.isPaused) {
                    // change the look of the button
                    this.addComponent("pauseButton").removeComponent("playButton");
                    // change the state of the button entity
                    this.isPaused = false;

                    // Serialize the whole game and send it over to the backend over the ctl websocket 
                    var game = plusButton.serialize();
                    game = JSON.stringify({'message': 'play', 'content': game});
                    Game.ctlSocket.send(game);
                } else {
                    // change the look of the button 
                    this.addComponent("playButton").removeComponent("pauseButton");
                    // change the state of the button entity                    
                    this.isPaused = true;

                    // Serialize the whole game and send it over to the backend over the ctl websocket 
                    var game = plusButton.serialize();
                    game = JSON.stringify({'message': 'pause', 'content': game});
                    Game.ctlSocket.send(game);
                }
            });
    }
});
