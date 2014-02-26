
"use strict";
Crafty.scene("intro", function() {

    var WIDTH = 1280;
    var HEIGHT = 720;

    // splash screen
    
    // set splashscreen timeout
    setTimeout(function() {
        Crafty.scene("menu");
    }, 500);

});