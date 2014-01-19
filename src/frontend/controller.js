/**

 THIS FILE'S NAME IS TENTATIVE!!!!!

 */


$(document).ready(function() {
    ws = new WebSocket("ws://localhost:8080/ws");

    ws.onmessage = function(e) {
       data = JSON.parse(e.data);
       console.log(data);
    };



/*
    // sess;
    // connect to WAMP server
    var address = "wss://127.0.0.1:8080/ws";
    // TODO autoban is forcing wss instead of ws, ws simply gives an error.

    ab.connect(address,
        // WAMP session was established
        function (session) {
            sess = session;
            console.log("Connected!");
        },

        // WAMP session is gone
        function (code, reason) {
            console.log(reason);

         // things to do once the session fails
        }
    );
*/
});