Crafty.c('PlayPause', {
    isPaused: true, 
    playingScenario: null,

    init : function() {
        this.requires('2D, Canvas, Mouse, playButton');
        var positionY = Crafty.viewport.height-200;
        
        this.attr({x: 20, y: positionY, w: 100, h: 100})
            .bind("Click", function() {
                if (this.isPaused) {
                    this.play();
                } else {
                    this.pause();
                }
            });
    }, 

    play: function() {
        console.log("play pressed");
        // change the look of the button
        this.removeComponent('playButton').addComponent('pauseButton');
        // change the state of the button entity
        this.isPaused = false;
/*
        if (!(this.playingScenario === plusButton.selectedScenario)) {
            // If the selected scenario has changed, send over the new scenario's interventions
            this.setInterventions();
            this.playingScenario = plusButton.selectedScenario;
        }
        */
        // send the play command
        var data = JSON.stringify({'message': 'play', 'content': ''});
        socket.emit("game_state", "play");
        
    },

    pause: function() {
        // change the look of the button 
        this.removeComponent('pauseButton').addComponent('playButton');
        // change the state of the button entity                    
        this.isPaused = true;
        // send the pause command
        var data = JSON.stringify({'message': 'pause', 'content': ''}); 
        socket.emit("game_state", "paused");
    }, 

    setInterventions: function() {
        var scenario = plusButton.selectedScenario.serialize();
        var data = JSON.stringify({'message': 'setInterventions', 'content': scenario});

        
        $(scope.data).each(function(index, element) { element.values = []; });
    }
});
