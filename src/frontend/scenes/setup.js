//Setup Screen

"use strict"
Crafty.scene("setup", function() {

//three buttons
	var buttons = {
		ROLE : 0,
		DIFFICULTY : 1,
		GOAL : 2
	}

	Crafty.e("2D, DOM, setupTitle").attr({	
		x : 375,
		y : 40	
	});

	//Role Button
	var roleButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 220
	}).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
		buttonAnimate(buttons.ROLE, "press");
	}).bind('MouseOut', function() {
		buttonAnimate(buttons.ROLE, "release");
	});

	var roleText = Crafty.e("2D, DOM, playText, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 220
	}).animate("press", [[54, 120]]).animate("release", [[0, 120]]).bind('MouseDown', function(){
		buttonAnimate(buttons.ROLE, "press");
	}).bind('MouseOut', function() { 
		buttonAnimate(buttons.ROLE, "release");
	}).bind('Click', function(){
		Crafty.scene("role");
	});

	//Diffuclty Button

	var difficultyButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 340
	}).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
		buttonAnimate(buttons.DIFFICULTY, "press");
	}).bind('MouseOut', function() {
		buttonAnimate(buttons.DIFFICULTY, "release");
	});

	var difficultyText = Crafty.e("2D, DOM, playText, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 340
	}).animate("press", [[54, 142]]).animate("release", [[0, 142]]).bind('MouseDown', function(){
		buttonAnimate(buttons.DIFFICULTY, "press");
	}).bind('MouseOut', function() { 
		buttonAnimate(buttons.DIFFICULTY, "release");
	}).bind('Click', function(){
		Crafty.scene("difficulty");
	});

	//End Goal Button
	var goalButton = Crafty.e("2D, DOM, menuBtn, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 460
	}).animate("press", [[ 54, 0 ]]).animate("release", [[0, 0]]).bind('MouseDown', function(){
		buttonAnimate(buttons.GOAL, "press");
	}).bind('MouseOut', function() {
		buttonAnimate(buttons.GOAL, "release");
	});

	var goalText = Crafty.e("2D, DOM, playText, SpriteAnimation, Mouse").attr({
		x : 515,
		y : 460
	}).animate("press", [[54, 164]]).animate("release", [[0, 164]]).bind('MouseDown', function(){
		buttonAnimate(buttons.GOAL, "press");
	}).bind('MouseOut', function() { 
		buttonAnimate(buttons.GOAL, "release");
	}).bind('Click', function(){
		Crafty.scene("goal");
	});


	//Animate buttons
	var buttonAnimate = function(btn, action){
		var button, text;
		switch (btn) {
			case buttons.ROLE:
				button = roleButton;
				text = roleText;
				break;

			case buttons.DIFFICULTY:
				button = difficultyButton;
				text = difficultyText;
				break;

			case buttons.GOAL:
				button = goalButton;
				text = goalText;
				break;

		}

		button.animate(action, 1, 0);
		text.animate(action, 1, 0);
	}
});