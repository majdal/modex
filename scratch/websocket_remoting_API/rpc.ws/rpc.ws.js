/* ideal API:
 *   tank = RPC("ws://example.com/games/0xG56/sprites/tank65")
 *   tank.turn(47.9); //-> cast to
 *   tank.HP().then(function(h) { console.log("I have", h.current, "hit points of", h.total) })
 
 * other ideal API (but expensive unless we multiplex websockets)
 *  tank_turn = RPC("ws://example.com/games/0xG56/sprites/tank65/hp/turn")
 *  tank_turn(47.9).error(function(e) { console.log("Error while turning tank:", e); })
 *  tank_HP = RPC("ws://example.com/games/0xG56/sprites/tank65/hp")
 *  tank_HP().then(function(h) { console.log("I have", h.current, "hit points of", h.total) }).error(....)
 
 this API ONLY supports positional arguments; AutobahnWamp tries to support keyword arguments, but depending on your perspective
  either js already has keyword args (just pass an object (aka a dict)) or it has no keyword args
  so we'll just ride on that..
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
  
  class Tank: #class we want to wrap out to the frontned
    [...]
    def turn(self, degrees):
        # we also have self.peer and all the other metadata that's in WebSocketServerProtocol so we can do Auth&Auth
        #, which RPCEndpoint attaches to us
        # or maybe peer comes in as a kwarg?
        # 
        self.heading+=degrees
    def HP(self):
        return {'current': self.hp, 'total': self.total_hp}
  tank = Tank("Big Cannon", 50hp, x, y, z)
  
  
  /* API #1:
  
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
  

// a way to wrap objects to make sub-ws sockets available?
function RPC2(ws)


function RPC_OOP(ws, prototype) {
	/* ws is a 'root' websocket
	 *
	 * prototype is 
	 */
	
}

/* backend (API #2):
 I like API 2 because it exposes each method as a distinct URL which feels more RESTish to me
  and it eschews sending metadata over the wire, because the socket you're connecting to 
 I don't like the proliferation of objects internally which do basically nothing but placemarkers for that metadata
  
class RPCEndpoint(WebSocketServerProtocol):
    def __init__(self, target): #target is a callable, not a class
        self._target = target
    
    def onMessage(self, payload, isBinary):
        

def RPCObjectEndpoint(o): #doesn't actually provide, but instead wraps each public method of o in a RPCEndpoint 
    

RPCEndpoint(tank.hp)


and similarly for the frontend, we need a bit of magic to get things rolling
(sadly, js has no __getattr__ magic, so we'll need to explicitly define the methods)

tank = RPC("ws://example.com/tank2", ["hp", "turn", "shoot"]) //you really shouldn't be holding any local state in tank yourself; if you insist, you can attach it after; but better to wrap, like function Tank() {... this._remote_tank = RPC(...) }
function RPC(ws, methods) {
    
	methods.each(
	 this[m]._ws = new WebSocket(ws+"/"+m) //XXX should be URLjoin
	 this[m]._ws.onmessage = function(evt) {
	 	
	 	//we still want a queue here....
	 }
	  this[m] = function() {
	    arguments = Array.prototype.slice(arguments);
	  	this[m].sendJSON.stringify(arguments);
	  	return new Promise()
	  }
	}
}
tank.hp().then(function(...))

tank.hp = function() {
	# serialize arguments
	
	
}
 */
