/* multiplex.ws: client library
 *
 */

WebSocketMultiplex = function(endpoint, _WebSocket, _serializer) {
  /* *class factory* which creates WebSocket-compatible classes that proxy all their calls through
   * We do this by wrapping
   * endpoint is the URL (absolute or relative) to a serverside multiplex.ws endpoint
   * and _WebSocket is an optional parameter which gives a WebSocket-compatible class (which could be, e.g., another WebSocketRealm) to construct WebSockets out of
   *  note: if _WebSocket is not provided, whatever value the global 'WebSocket' has at the time of calling WebSocketRealm() is stored as the backing class.
   *
   * Goal: this should be DROP IN transparent.
       you should be able to say WebSocket = WebSocketMultiplex(..) and have all your code work with it commented in or out
   * Depends:
   *   URL.prototype.join        (hard)
   *   URL.prototype.toWebSocket (soft)
   *
   * Usage:
   *   
   * 
   * TODO:
   *  [ ] Figure out how instanceof sees results from this class, and if so what to do about that. Is anyone going to be depending on us?
   *  [ ] Double check js scoping rules to make sure that WebSocket is actually the global WebSocket, no matter how many layers deep we are.  [ ] Tidy the protocol. It can be more succinct.
   *  [ ] Make the returned class use prototypes
   *  [ ] Clone _WebSocket's prototype before filling in our own bits
   *  [ ] What happens if the underlying socket conks out?
   *  [ ] In practice, we really only care about JSON and msgpack; to get the best of both worlds without being onerous to users, perhaps we should just decide that the handshake is always in json, but the server responds with {"multiplex": "json"} or {"multiplex": "msgpack"} and every message after that is expected to use those
       actually, there's no reason the protocol has to be json based.
       it could just be a simple "first byte tags messagetype" protocol (or maybe 'first 2 bits'? that probably is not worth the overhead of figuring out how to do bitfiddling in js, because the REST of the message is still going to align on a byte boundary)
   * how many message types do we have:
      -clienthandshake
      -serverhandshake
      -clientopen
      -serveropen (response to open request)
      -message
      -close
   */
   
   
  /* protocol: we need to implement all the basic things the WebSocket protocol gives. I think just wrapping, though, should do it: (NB: the messages are given in json notation without explanation; they might actually be in msgpack or some other serialization format)
   *
   * upon first connecting, a short handshake (is this really necessary?)
   * client: "multiplex"
   * server: "multiplex"
   *
   * client: {"open": url} --> put on a queue; WebSocket guarantees (via TCP and its own shenannigans) in-order delivery. So server guarantees to resolve open requests in order with:
     the server thinks about 'url', tries to find an endpoint to go with it, and if it find one, spins it up, wrapped in a proxy object, and sends back:
     server: {"open": channel_id}
   if it can't find one it sends
     server: {"open": error} 
   *
   * client||server {"message": data, "channel": id}
   * 
   * client||server: {"close": channel_id}
   */
  

  if(!(endpoint instanceof URL)) {
    endpoint = new URL(endpoint);
  }
  
  if(endpoint.toWebSocket) {
    endpoint = endpoint.toWebSocket();
  } else {
    console.warn("URL.prototype.toWebSocket is not installed. Make sure '"+endpoint.href+"' uses the correct websocket scheme.")
  }
  
  if(_WebSocket == null) {
    _WebSocket = WebSocket; //stash original WebSocket class in our closure (if we don't do this, and someone uses WebSocketRealm to overwrite the default WebSocket, infinite loops will happen)
  }
  
  if(_serializer = null) {
      _serializer = JSON
  }
  
  var connecting = []; //FIFO queue of channels we're
  var channels = {};   //set of channels, indexed by their channel ID
  
  var _ws = new _WebSocket(endpoint.href);
  var sessionOpen = false;
  
  _ws.onopen = function(evt) {
      _ws.send("multiplex") //XXX do we really need to bother with a handkshake?
  }
  
  _ws.onmessage = function(evt) {
      message = _serializer.parse(evt.data)
      if(!sessionOpen) {
        if(message == "multiplex") sessionOpen = true;
        else {
            // throw an error
            // not sure who to throw it to, exactly
            // maybe just to the nether
            throw new Error("multiplex.ws handshake failed");
        }
      } else {
          message
          if(message['open']) {
            ws = connecting.shift();
            if(message['open'] instanceof "string") { //skeeetch
                var error = message['open'];
                evt = {'type': 'error', }
                ws.onerror(evt) //TODO: andle this being null
                // the WebSocket in FireFox doesn't change its readyState if it never opens...
                // hmm.
                // what 
            } else { // assume it's an successfully opened channel message
              var id = message['open'];
              channels[id] = ws;
              ws.readyState = WebSocket.OPEN;
              evt = {}; // TODO: fill in
              ws.onopen(evt); //TODO: handle this being null
            }
          } else if(message['close']) {
            var id = message['close'];
            //TODO: error checking; what if the server lies?
            delete channels[id];
            ws.readyState = WebSocket.CLOSED;
              evt = {}; // TODO: fill in
              ws.onclose(evt); //TODO: handle this being null
          }
      }
  }
  
  _ws.onerror = function(evt) {
      // pass the error to all children?
      channels.forEach(function(ch) {
          ch.onerror(evt)
      })
  }
  
  _ws.onclose = function(evt) {
      // close all channels summarily
      
      channels.forEach(function(ch) {
          ch.onclose(evt)
          
      })
      
      channels = [];
  }
  
  function send(d) {
      // convenience method
      _ws.send(serializer.stringify(d));
  }
  
  
  function WebSocketClass(href) { 
     
     var ws = {}
     if(typeof(ws) != "object") { // <- this check ensures that this function behaves itself, despite not being a 'proper' constructor.
                                 // see http://stackoverflow.com/questions/1978049/what-values-can-a-constructor-return-to-avoid-returning-this / http://bclary.com/2004/11/07/#a-13.2.2
       throw new Error("The WebSocket implementation that WebSocketRealm("+endpoint.href+") is wrapping did not construct an object.")
     }
     
     ws.url = endpoint.join(href).href; //TODO: use defineProperty to make this immutable
     ws.readyState = WebSocket.CONNECTING; //???
     ws.onopen = null;
     ws.onmessage = null;
     ws.onerror = null;
     ws.onclose = null;
     
     ws.channel = null; //extra property that mul, used internally and used 
     
     send({"open": href})
     connecting.push(ws) //ws isn't actually a websocket, it's our fake websocket we're handing to the user
     
     ws.send = function(data) {
         if(!(data instanceof string)) {
             throw new Error("Can only send bytes over WebSockets") //TODO match this error to the real error
         }
         
         //TODO: check that our readyState is correct
         // TODO: check a zillion other things
         if(! ws.readyState == WebSocket.OPEN) {
             throw new Error("WebSocket not open");
         }
         
         send({'message': data, 'channel': ws.channel})
     }
     
     ws.close = function() {
         ws.readyState = WebSocket.CLOSING;
         send({'close': ws.channel})
     }
     
     return ws;
  }

  return WebSocketClass
}
