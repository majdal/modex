//Setup Screen

"use strict"
Crafty.scene("goals", function() {
//three buttons
	

	Crafty.e("2D, DOM, goalTitle").attr({	
		x : 375,
		y : 30	
	});

	//back button

	Crafty.e("2D, DOM, squareBtn").attr({
    	x: 10,
        y: 600
    });

    Crafty.e("2D, DOM, backArrow, Mouse").attr({
    	x: 10,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("setup")
    });

    //load goals
    Crafty.e("2D, DOM, menuBtn, Mouse").attr({
    	x: 225,
        y: 600
    });

    Crafty.e("2D, DOM, loadscText, Mouse").attr({
    	x: 225,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("loadgoals")
    });


    //save goals
    Crafty.e("2D, DOM, menuBtn, Mouse").attr({
    	x: 525,
        y: 600
    });

    Crafty.e("2D, DOM, saveText, Mouse").attr({
    	x: 525,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("savegoals")
    });


    //start game
    Crafty.e("2D, DOM, menuBtn, Mouse").attr({
    	x: 825,
        y: 600
    });

    Crafty.e("2D, DOM, startText, Mouse").attr({
    	x: 825,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("game")
    });


	//Modal Window
   Crafty.e("2D, DOM, modalWindow").attr({
   		x: 265,
   		y: 115
   });


   // Happiness

   Crafty.e("2D, DOM, happinessIcon").attr({
   		x: 340,
   		y: 125
   });

   Crafty.e("2D, DOM, happinessText").attr({
   		x: 450,
   		y: 135
   });

   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 225
   });

   //Corn Output

   Crafty.e("2D, DOM, cornIcon").attr({
   		x: 340,
   		y: 235
   }).bind('Click', function() {
    	Crafty.scene("goals");
    });

   Crafty.e("2D, DOM, cornText").attr({
   		x: 450,
   		y: 235
   });

   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 335
   });

   //GDP

   Crafty.e("2D, DOM, gdpIcon").attr({
   		x: 340,
   		y: 345
   });

   Crafty.e("2D, DOM, gdpText").attr({
   		x: 450,
   		y: 345
   });

   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 445
   });

   
});

