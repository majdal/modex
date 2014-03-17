//Setup Screen

"use strict"
Crafty.scene("setup", function() {

	

	Crafty.e("2D, DOM, setupTitle").attr({	
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
    	Crafty.scene("menu")
    });

    //load scenario
    Crafty.e("2D, DOM, menuBtn, Mouse").attr({
    	x: 225,
        y: 600
    });

    Crafty.e("2D, DOM, loadscText, Mouse").attr({
    	x: 225,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("loadscenario")
    });


    //save scenario
    Crafty.e("2D, DOM, menuBtn, Mouse").attr({
    	x: 525,
        y: 600
    });

    Crafty.e("2D, DOM, saveText, Mouse").attr({
    	x: 525,
        y: 600
    }).bind('Click', function() {
    	Crafty.scene("savescenario")
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


   // Government

   Crafty.e("2D, DOM, govtIcon").attr({
   		x: 340,
   		y: 125
   });

   Crafty.e("2D, DOM, govtText").attr({
   		x: 450,
   		y: 135
   });

    
   //text
   Crafty.e("2D, DOM, text1").attr({
    x: 450,
    y: 165
   });


   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 225
   });
   //Starting Conditions

   Crafty.e("2D, DOM, condIcon, Mouse").attr({
   		x: 340,
   		y: 235
   }).bind('Click', function() {
    	Crafty.scene("goals");
    });

   Crafty.e("2D, DOM, condText").attr({
   		x: 450,
   		y: 245
   });

   Crafty.e("2D, DOM, text2").attr({
    x: 450,
    y: 295
   });

   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 355
   });

   /*
   //Natural Disasters

   Crafty.e("2D, DOM, natIcon").attr({
   		x: 340,
   		y: 345
   });

   Crafty.e("2D, DOM, natText").attr({
   		x: 450,
   		y: 345
   });

   Crafty.e("2D, DOM, breakLine").attr({
   		x: 450,
   		y: 445
   }); */

   //Game Time

   Crafty.e("2D, DOM, timeIcon").attr({
   		x: 340,
   		y: 365
   });

   Crafty.e("2D, DOM, timeText").attr({
   		x: 450,
   		y: 375
   });

   Crafty.e("2D, DOM, text3").attr({
    x: 450,
    y: 395
   });
});

