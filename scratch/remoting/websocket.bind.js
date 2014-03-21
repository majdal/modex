/*
Problem:
the raw WebSocket API has you assigning event handlers direct to functions.
 Which then runs your handlers in the context of the websocket object (they change 'this'),
 which is confusing when you're deep in application code.

Solution: 
 follow jQuery's lead and allow appending chains of event handlers with .bind()
 [TODO: make sure 'this' behaves itself]
  
API goal:

 z = new WebSocket("wss://site.com/whateverdatastreem")
    .open(function(evt) { console.log(z.url, "connected") })
    .close(function(evt) { ... })
    .message(function(messageevent) { ... })
    .error(function(evt) { ... })
    .open(function(evt) { console.log("ooh, i forgot to say: happy barfday") })
    
*/

WebSocket.prototype.bind = function(event, handler) {
  //TODO: ...
  return this; //to allow chaining
}

WebSocket.prototype.open = function(handler) {
  return this.bind("open", handler);
}
WebSocket.prototype.message = function(handler) {
  return this.bind("message", handler);
}
WebSocket.prototype.error = function(handler) {
  return this.bind("error", handler);
}
WebSocket.prototype.close = function(handler) {
  return this.bind("close", handler);
}
