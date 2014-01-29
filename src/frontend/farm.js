//Main game module
"use strict";
var farm = function($){
	return {

		config : {
			width : 1280,
			height : 720
		},
		//initialize crafty
		Crafty.init(this.config.width, this.config.height);
		Crafty.canvas.init();

		//set background
		Crafty.background("url('images/background.png')");


		//Run Menu
		Crafty.scene("menu");

		//load sprite sheet
		Crafty.sprite(5, "images/sprite.png", {

			//Titles
			logoText : [0, 90, 106, 116],
			setupTitle : [156, 0, 251, 20],

			//Menu buttons
			menuBtn : [0, 0, 50, 20],
			playText: [0, 24, 50, 20],
			setupText: [0, 46, 50, 20],
			loadText : [0, 68, 50, 20],
			scenariosText : [106, 24, 50, 20],

			//Setup Screen Text
			roleText : [0, 120, 50, 20],
			difficultyText : [0, 142, 50, 20],
			goalText : [0, 164, 50, 20]

		});
	};
}($);