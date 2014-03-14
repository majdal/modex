
"use strict";
Crafty.scene("intro", function() {

    var WIDTH = 1280;
    var HEIGHT = 720;

    // set splashscreen timeout
    setTimeout(function() {
        Crafty.scene("game");
    }, 500);

});