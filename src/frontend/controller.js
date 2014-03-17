
$(document).ready(function() {
    window.Game = {}; // global variable to hold all game components. Currently mostly used for easy serialization 

    // the control websocket 
    Game.ctlSocket = new WebSocket('ws://' + location.host + '/ctl');

    Game.ctlSocket.onmessage = function(e) {
       data = JSON.parse(e.data);
       console.log(data);
    };

    // the data websocket
    Game.dataSocket = new WebSocket("ws://" + location.host + "/ws"); //our websocket sits at /ws (TODO(kousu): reorg this)

});