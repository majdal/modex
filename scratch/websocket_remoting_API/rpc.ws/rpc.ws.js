/* ideal API:
 *   tank = RPC("ws://example.com/games/0xG56/sprites/tank65")
 *   tank.turn(47.9); //-> cast to
 *   tank.HP().then(function(h) { console.log("I have", h.current, "hit points of", h.total) })
 
 * other ideal API (but expensive unless we multiplex websockets)
 *  tank_turn = RPC("ws://example.com/games/0xG56/sprites/tank65/hp/turn")
 *  tank_turn(47.9).error(function(e) { console.log("Error while turning tank:", e); })
 *  tank_HP = RPC("ws://example.com/games/0xG56/sprites/tank65/hp")
 *  tank_HP().then(function(h) { console.log("I have", h.current, "hit points of", h.total) }).error(....)

// protocol 1:
// first, connect to the websocket supporting this protocol 
// calls: {'method': methodname, 'arguments': [arg1, arg2, ...]} in json
// responses: {'error': 'error message'} || {'payload': return_value}

// protocol 2 (aka your mother's simplest protocol):
// 
// calls: [arg1, arg2, ...] in json
// responses: {'error': 'error message'} || {'result': return_value} in json
// protocol 2a (to support object mapping)
//  -> no change to the basic protocol
//  -> objects get unique URLs ("//example.com/data/maps/vector/buildings/northyork") which simply give a "This is a WebSocket Object Endpoint" page when accessed over HTTP
//  -> their methods are under them in the hierarchy (say, internally, northyork has northyork.m1(), northyork.m2(), then )
// "ws://example.com/data/maps/vector/buildings/northyork/m1" and "ws://example.com/data/maps/vector/buildings/northyork/m2" are URLs supporting protocol 2

Either API ONLY
 a) supports positional arguments
  AutobahnWamp tries to support keyword arguments, but depending on your perspective
  either js already has keyword args (just pass an object (aka a dict)) or it has no keyword args
  so we'll just ride on that..
 b) handles calls strictly in order (so a slow call will hold up a fast one if it happened to be invoked first); if you need non-strict RPC ordering, design your system with two RPC websockets: a fast and a slow one);
 AutobahnWamp supports non-strict ordering, and it does this by generating (in-browser) a (hopefully, but you know how that goes) crypto-strong message ID hash, and sending it with each message, which forces each message to be a meta-structure (ie. {'method': method, 'id': id, parameters: [real arguments go here]}) 


  I like API 1 because it makes the number of necessary websockets less (but we were already planning on using a Multiplexer)
   and it seems like it should make the internal implementation shorter: there's only one (WebSocketResource, WebSocketServerFactory, WebSocketServerProtocol) instead of one of those triplets for EACH method
   and it makes more sense, then, to pass in the data from the WebSocketServerProtocol (like .peer, .connected, .time, .http_headers)
   --and it allows you to call methods not specified -- but maybe that's a bug, not a feature, in the context of RPC
    I would like API 1 more if js supported autopassing not-found attrs to something like __getattr__ in python/ruby;
      -> because you can't do this, AutobahnWamp insists you do session.call("methodname", args)

  
  I like API 2 because it exposes each method as a distinct URL which feels more RESTish to me;
   it will certainly be easier to debug and log, long term, because we can eg. use Wireshark filtering on HTTP URLs instead of having to filter
  and it eschews sending metadata over the wire, because the socket you're connecting to IS the metadata
    I don't like the proliferation of objects internally which do basically nothing but placemarkers for that metadata -- but that probably doesn't actually hurt the performance
   I also very much like that API doesn't -force- you to be OOP: in API2 the default case is an exposed function call, and it's only by extension (Protocol 2a) that you get the case of an exposed object. In API1, exposing only a single function would mean writing a whole class (java-style) just containing one method. This seems like it should be much much easier to compose with other objects; e.g. into an AuthorizedRPCObject()
    
 
 */

/* TODO:
 
 * [x] use Promises instead of uglily passing a handler
    * [ ] use a standard Promises library instead of this hack thing
 * [ ] use __getAttr__ to autobind -- impossible??
 * [x] autowrap a websocket if a string is passed
 * [ ] reindent to 4 spaces
 * [ ] typecheck ws URLs
 * [ ] enforce that RPC and ObjectRPC are created via `new`
 * [ ] figure out if I can make (via .prototype) a specialized WebSocket class -- RPCWebSocket -- that has onmessage filled in by prototype instead of by constantly recreating it

 * [ ] support composable WebSocket-like instances; as a consequence, then:
   * [ ] support relative URLs
     * [ ] and clean up how ObjectRPC does it
   * [ ] //semirelative.com/urls
   * [ ] support multiplexing
 */

/*
 * do we assume functional? ie same args => redundant call?
 */

/* js OOP ref: http://www.documentroot.net/en/misc/js-tutorial-classes-prototypes-oop
 */

WebSocket = require("ws");
var serializer = JSON //serialize should be an object with "parse" and "stringify" methods

Promise = require("./promise.js")
  
function RPC(ws) {
    /*
     *
     * usage:
     *   talk = RPC("ws://example.com:5755/path/to/endpoint");
     *   talk("hey").then(function(r) { handle return value r })
     *
     * you can debug you connection with:
     *   talk.error(function(evt) { ... }) which binds your given function to the WebSocket onerror handler
     *
     * you can also pass a premade WebSocket in:
     *   var h = new WebSocket("wss://shortcut.net/socklet")
     *   h.onerror
     *   shout = RPC()
     * (but it won't do much good.....)
     * ...hmmm maybe this is a bad idea
     * hmmm but if you can't do that, how do we MULTIPLEX
     */
     
      
	var queue = []; //queue of calls in progress; actually a queue of promises, since we .send() immediately (assuming js is single threaded but eventLooped)
	var open = false;
     
	if(ws instanceof String || typeof(ws)=='string' || ws.substr) { // TODO: figure out the proper way to do polymorphism/ducktyping in js; I know you can check for the existence of properties, but is that the Right Way? 
		ws = new WebSocket(ws);
	}

	
	 
     ws.onopen = function(evt) {
         ready_handler();
         open = true;
     };
     ws.onclose = function(evt) {
         open = false;
         ws = null;
     };
     
	 
	 //actually, we don't need to enforce one-call-at-a-time
	 //we can instead just immediately send data and put the promise on the queue
	 // and so long as we can assume that send() is atomic, this should be fine
	 ws.onmessage = function(evt) {
	    if(queue.length <= 0) {
	    	throw new Error("Received RPC message but no call is in the queue waiting for it");
	    }
	 	response = serializer.parse(evt.data);
	 	promise = queue.shift();
	 	//console.log(response) //debug
	 	// TODO: experiment with calling these on setTimeout(function() { }, 10) //
	 	if('error' in response) {
	 	    promise.error(response.error); //err how do i distnguish promises and promiss?
	 	} else if('result' in response) {
                    promise.resolve(response.result);
	 	} else {
	 	    console.log("Got malformed RPC message:", evt.data)
     	}
     }
     
     var error_handler = function(evt) { /*no-op*/ } //TODO: use promises here??
     ws.onerror = function(evt) {
       error_handler(evt);
     }
     
	function call() {
	    if(!open) {
	      throw new Error("WebSocket not open")
	    }
	    arguments = Array.prototype.slice(arguments);
	  	ws.send(JSON.stringify(arguments));
	  	var p = new Promise();
	  	queue.push(p);
	  	return p;
	}
	
    var ready_handler = function(evt) { /*no-op*/ } //TODO: use promises here??
	call.ready = function(f) {
	    ready_handler = f;
	}
	call._ws = ws; //expose the websocket just cuz
	call.error = function(f) {
	    error_handler = f;
	}
	
	// test if we're open, just in case the socket was open BEFORE it was given to us
    open = (ws.readyState == ws.OPEN); // XXX there's (possibly, depending on the particular js interpreter's threading model) a small window between which this is checked and onopen is set
    
	return call;
}

function ObjectRPC(ws, methods) {
    /*
     * takes: a websocket URL 
     * you really shouldn't be holding any local state in tank yourself; if you insist, you can attach it after; but better to wrap, like function Tank() {... this._remote_tank = RPC(...) }
     *
     */
     //
    // here, ws a URL but is not actually expected to be a websocket; it 
    if(this == global) throw new Error("you dun wrong; use `new`")
    var readyCount = 0; //sketchy! the idea is to fire ObjectRPC._readyHandler() when all sub sockets are ready
    
    var self = this; //avoid scoping trouble; 'methods.forEach' runs its function with this = methods
    methods.forEach(function(m) {
	   self[m] = RPC(ws+"/"+m); //XXX should be URLjoin
	   self[m].ready(function(){
	     readyCount += 1;
	     if(readyCount >= methods.length) { ready_handler(); }
	   })
	   self[m].error(function(e) {
	     error_handler(e);
	   })
	   })
		
	var error_handler = function(evt) { /*no-op*/ } //TODO: use promises here??
	this.error = function(f) {
	    error_handler = f;
	}
        
	var ready_handler = function(evt) { /*no-op*/ } //TODO: use promises here??
	this.ready = function(f) {
	    ready_handler = f; //what. this triggers it again??
	}
	return this;
}

module.exports = {'ObjectRPC': ObjectRPC, 'RPC': RPC}
  
  /* and the backend looks like
  
  #class we want to wrap out to the frontned
  */
  
  
  /* Backend under API #1:
  
  class RPCEndpoint(WebSocketServerProtocol):
      "wraps an object and serves its public (ie non-_) methods up over a websocket"
      def __init__(self, target): self._target = target
      def onMessage(self, payload, isBinary):
          payload = serializer.loads(payload) //use the same serializer as the js side uses (nb loads is python for parse, like dumps ("dump to string") is python for stringify)
          method = payload['method']
          args = payload['arguments']
          try: #catch
              if method.startswith("_"): #hide
                  raise PrivateMethodError()
              result = getattr(self._target, method)(*args) #splay arguments across
              result = serializer.dumps(result)
              self.send(result)
           catch AttributeError, exc:
              pass
              
  endpoint = RPCEndpoint(tank)
  attach_node_to_twisted_hiearchy(endpoint)
  */
