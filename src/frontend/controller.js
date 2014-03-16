
$(document).ready(function() {
    Game = {}; // global variable to hold all game components. Currently mostly used for easy serialization 
    ctl = new WebSocket("ws://localhost:8080/ctl");

    ctl.onmessage = function(e) {
       data = JSON.parse(e.data);
       console.log(data);
    };
});