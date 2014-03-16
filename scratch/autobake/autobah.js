/* autobah.js
 *  runs under nodejs
 */
WebSocket = require("ws");
ws = new WebSocket("ws://localhost:8080/echo");
ws.onmessage = function(evt) {
  console.log("received", evt.data);
}

ws.onopen = function(evt) {
  setInterval(function() {   ws.send("fancy free"); },  4000);
}
