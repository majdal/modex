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
// responses: {'error': 'error message'} || {'payload': return_value} in json
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
  
  I like API 2 because it exposes each method as a distinct URL which feels more RESTish to me;
   it will certainly be easier to debug and log, long term, because we can eg. use Wireshark filtering on HTTP URLs instead of having to filter
  and it eschews sending metadata over the wire, because the socket you're connecting to IS the metadata
    I don't like the proliferation of objects internally which do basically nothing but placemarkers for that metadata -- but that probably doesn't actually hurt the performance
   I also very much like that API doesn't -force- you to be OOP: in API2 the default case is an exposed function call, and it's only by extension (Protocol 2a) that you get the case of an exposed object. In API1, exposing only a single function would mean writing a whole class (java-style) just containing one method. This seems like it should be much much easier to compose with other objects; e.g. into an AuthorizedRPCObject()
    
 
 */

/* TODO:
 
 * [ ] use Promises instead of uglily passing a handler
 * [ ] use __getAttr__ to autobind -- impossible??
 * [x] autowrap a websocket if a string is passed
 */

/*
 * do we assume functional? ie same args => redundant call?
 */

/* js OOP ref: http://www.documentroot.net/en/misc/js-tutorial-classes-prototypes-oop
 */

var serializer = JSON //serialize should be an object with "parse" and "stringify" methods

function RPC(ws) { //la la la
  if(ws instanceof String) {
    ws = new WebSocket(ws);
  }
  
  /*
  ws.onopen = 
  ws.onclose = 
  ws.onerror = 
  */
  
  //this looks a bit funny (ie its not just a simple loop) because we're stream-orienting a message-oriented protocol
  
  /*
  how i'd write this in a magic language with built in concurrency magic
  (python's generators are pretty close to this)
  _queue = []
  def queue():
     while _queue:
       yield queue[0]
       queue.pop(0)
       
  def rpc():
     for request in queue():
       ws.send(serialize(request))
       result = yield
       handler(result)
       yield
       
  def wrap():
    onMessage(m):
      r.send(m) #we guarantee that there's only one active message from us at a time
  */
  
  ws.onmessage = function(evt) {
    
    response = serializer.parse(evt.data)
    
    //call handler
    if('error' in response) {
    	error(response.error);
    }
    else if('result' in response) {
        handler(response.result);
    }
    
    queue.shift()
    
    //now push the next things on the queue
    pump()
    
    
  }
  
  this.queue = []
  
  function pump() { //pump the queue: send the next request
  	if(queue.length > 0) {
  		this.queue.
  		serialize.stringify(this.queue[0])
  	}
  	
  	//serialize
  }  
}

// js doe	sn't support autopassing not-found to something like __getattr__
RPC.prototype.call = function(method, handler) {
  if(!(ws instanceof String)) {
    throw Error("remote method names must be strings");
  }
  
  arguments = Array.prototype.slice.call(arguments, 2); //coerce args to a real array, eating the args that aren't part of it
  arguments.shift(); //eat 'method' and 'handler' pass the remainder through RPC
  
  queue.push({method: method, args: arguments, handler: handler})
    
    //return a promise  	
  }
  
  /* and the backend looks like
  
  #class we want to wrap out to the frontned
  
  class Tank: 
    [...]
    def turn(self, degrees):
        # we also have self.peer and all the other metadata that's in WebSocketServerProtocol so we can do Auth&Auth
        #, which RPCEndpoint attaches to us
        # or maybe peer comes in as a kwarg?
        # 
        self.heading+=degrees
    def HP(self):
        return {'current': self.hp, 'total': self.total_hp}
  
  tank = Tank("Big Cannon", x, y, z, hp=50)
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



/* backend (API #2):
  
  
class RPCProtocol(WebSocketServerProtocol):
    "wrap a callable into a websocket: messages are parameters to function calls; return values"
    "handles serialization automatically"
    "and nothing else"
    def __init__(self, target): #target is a callable, not a class
        self._target = target
    
    def onMessage(self, payload, isBinary):
        # XXX maybe _target() should be called on a Deferred? we have no idea
        # how long _target() will take to execute, and hanging the whollle server
        # ..but maybe that's part of the game; hanging the server early
        # in test is better than load problems sneaking up later because
        # the app writer didn't thoroughly make sure they had caching in at the right layers
        
        # note: protocol assumes only one message at a time
        #  if we didn't, messages would need to come with an id code (like Autobahn does)
        # ...actually that's not true, these four lines enforce one-message-at-a-time:
        # there's no way to hear the next message until _target() returns
        #  (wtf does Autobahn do, then? Does it use Deferreds? It allows parallel calls, that's for sure)
        payload = serializer.loads(payload)
        result = self._target(*payload)
        result = serializer.dumps(result)
        self.send(result)


def RPCEndpoint(method, debug = False):
    "why the debug param? because "
    f = WebSocketServerFactory(" why do i have to tell you the URL, Autobake? ", debug = debug, debugCodePaths = debug )
    f.protocol = RPCProtocol(method)
    return f

class RPCObjectEndpoint(twisted.web.resource.Resource):
   "convenience class to make putting" #this class is feature-parable with RPCEndpoint in API #1
   "doesn't actually provide a websocket, but instead wraps each public method of o in a RPCEndpoint"
    def __init__(self, o):
      for method in (m for m in dir(o) if callable(getattr(o, m))): #find all the names (strings) of all methods
          self.addChild(method, RPCEndpoint(getattr(o, method))


endpoint = RPCObjectEndpoint(tank)
root.putChild("tank1", endpoint)

and similarly for the frontend, we need a bit of magic to get things rolling
(sadly, js has no __getattr__ magic, so we'll need to explicitly define the methods)

function RPC(ws) {
	if(ws instanceof String) {
		ws = new WebSocket(ws);
	}
	//TODO: support relative URLs and //semirelative.com/urls
	
	function call() {
	    arguments = Array.prototype.slice(arguments);
	  	this[m].send(JSON.stringify(arguments));
	  	return new Promise()
	}
	
	return call;
}

function ObjectRPC(ws, methods) {
    // here, ws a URL but is not actually expected to be a websocket; it  
    queue = []; //queue of calls in progress
	methods.forEach(function(m) {
	 this[m] = RPC(ws+"/"+m); //XXX should be URLjoin
	 
	 //actually, we don't need to enforce one-call-at-a-time
	 //we can instead just immediately send data and put the promise on the queue
	 // and so long as we can assume that send() is atomic, this should be fine
	 this[m]._ws.onmessage = function(evt) {
	    if(queue.length <= 0) {
	    	throw new Error("Received RPC message but no call is in the queue waiting for it");
	    }
	 	response = serializer.parse(evt.data);
	 	promise = queue.shift();
	 	
	 	
	 	// TODO: experiment with calling these on setTimeout(function() { }, 10) //
	 	if('error' in response) {
	 	    promise.error(response.error); //err how do i distnguish promises and promiss?
	 	} else if('payload' in response) {
	 		promise.resolve(response.payload);
	 	} else {
	 		console.log("Got malformed RPC message:", evt.data)
	 	}
	 	
	 }
	  this[m] = 
	}
}

// usage:
tank = RPC("ws://example.com/tank2", ["hp", "turn", "shoot"]) //you really shouldn't be holding any local state in tank yourself; if you insist, you can attach it after; but better to wrap, like function Tank() {... this._remote_tank = RPC(...) }
tank.hp().then(function(...) {...})

 */
