 window.onload = function() {

    var ws = new WebSocket("ws://localhost:9000");

    ws.onmessage = function(e) {
       console.log("Got echo: " + e.data);
    }
 }