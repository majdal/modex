README 
=========

This is a quick little screenshot dump of a popular opensource
Civ-2 clone, Freeciv. This is taken from an online HTML5 clone of it.

Process
----------
This can be used to as a template for the Crafty engine.

This should be not that hard to implement, and there are multiple
layers. (easy to explain the idea in person.)

Idea
---------
Basically the user requests to see different layers at a time.
The amount of layers is a natural number. So, the end user is viewing
at least one layer at a time.

Now, there are 2 different kinds of layers, base layers,
and overlay layers.

The user can only have one base-type layer showing at a time,
but they can have multiple overlay layers a time.

For instance,

Base layers include: 
  * land usage (ie city, farmland, quarries, watersheds)
  * topology (height map)
  * water basins
  	(only caring about water, I dont know enough geography)
		
Overlay layers include: 
  * rivers
  * geopolitical boundaries (city/county divisions etc)
  * roads

Why
------
The advantage of this system is that you can
take rasterized.
