
"use strict";
Crafty.scene("menu", function() {
    Crafty.background("url('images/background.png')");
    
   
    //four buttons in menu sceen
    var buttons = {
        PLAY : 0,
        SETUP : 1,
        LOAD : 2,
        //SCENARIOS : 3
    }

    //Logo
    Crafty.e("2D, DOM, logoText").attr({
        x : 375,
        y : 40
    });

    // Exit 
    Crafty.e("2D, DOM, squareBtn").attr({
        x: 10,
        y: 610
    });
    Crafty.e("2D, DOM, exitBtn").attr({
        x: 10,
        y : 610
    });

    

    //Play Now Button
    var playButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 220
    }).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
        buttonAnimate(buttons.PLAY, "press");
    }).bind('MouseOut', function() {
        buttonAnimate(buttons.PLAY, "release");
    });
    

    var playText = Crafty.e("2D, DOM, playText, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 220
    }).animate("press", [[54, 24]]).animate("release", [[0, 24]]).bind('MouseDown', function(){
        buttonAnimate(buttons.PLAY, "press");
    }).bind('MouseOut', function() { 
        buttonAnimate(buttons.PLAY, "release");
    }).bind('Click', function(){
        Crafty.scene("game");
    });

    //Set Up Button
    var setupButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 340
    }).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
        buttonAnimate(buttons.SETUP, "press");
    }).bind('MouseOut', function() {
        buttonAnimate(buttons.SETUP, "release");
    });

    var setupText = Crafty.e("2D, DOM, setupText, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 340
    }).animate("press", [[54, 46]]).animate("release", [[0, 46]]).bind('MouseDown', function(){
        buttonAnimate(buttons.SETUP, "press");
    }).bind('MouseOut', function() { 
        buttonAnimate(buttons.SETUP, "release");
    }).bind('Click', function(){
        Crafty.scene("setup");
    });

    //Load Button
    var loadButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 460
    }).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
        buttonAnimate(buttons.LOAD, "press");
    }).bind('MouseOut', function() {
        buttonAnimate(buttons.LOAD, "release");
    });


    var loadText = Crafty.e("2D, DOM, loadText, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 460
    }).animate("press", [[54, 68]]).animate("release", [[0, 68]]).bind('MouseDown', function(){
        buttonAnimate(buttons.PLAY, "press");
    }).bind('MouseOut', function() { 
        buttonAnimate(buttons.PLAY, "release");
    }).bind('Click', function(){
        Crafty.scene("load");
    });

    /*Scenarios Button
    var scenariosButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 580
    }).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
        buttonAnimate(buttons.SCENARIOS, "press");
    }).bind('MouseOut', function() {
        buttonAnimate(buttons.SCENARIOS, "release");
    });


    var scenariosText = Crafty.e("2D, DOM, scenariosText, SpriteAnimation, Mouse").attr({
        x : 515,
        y : 580
    }).animate("press", [[106, 46]]).animate("release", [[106, 24]]).bind('MouseDown', function(){
        buttonAnimate(buttons.SCENARIOS, "press");
    }).bind('MouseOut', function() { 
        buttonAnimate(buttons.SCENARIOS, "release");
    }).bind('Click', function(){
        Crafty.scene("scenarios");
    });*/


    //Animate buttons (press and release)
    var buttonAnimate = function(btn, action){
        var button, text;
        switch (btn) {
            case buttons.PLAY:
                button = playButton;
                text = playText;
                break;

            case buttons.SETUP:
                button = setupButton;
                text = setupText;
                break;

            case buttons.LOAD:
                button = loadButton;
                text = loadText;
                break;

            /*case buttons.SCENARIOS:
                button = scenariosButton;
                text = scenariosText;
                break; */
        }

        button.animate(action, 1, 0);
        text.animate(action, 1, 0);
    }

});