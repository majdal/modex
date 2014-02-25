
"use strict";
Crafty.scene("intro", function() {

    var WIDTH = 1280;
    var HEIGHT = 720;

    // splash screen
    var splashScreen = Crafty.e("2D, DOM, Image, Tween, Mouse").attr({
        alpha : 0
    }).image('images/splash.jpg');

    // set splashscreen timeout
    setTimeout(function() {
        Crafty.scene("menu");
    }, 3000);

});