/**@
* #PlayPause
* @category Custom
*
* A simple play/pause button for the game
*
*/
Crafty.c("PlayPause", {
	init: function(entity) {
		this.requires("2D");
		this._pbFilledFraction = 0;
	},

	play: function() {
		console.log('play');
	},

	pause: function() {
		console.log('pause');
	},
});