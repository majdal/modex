

import sys
from os.path import dirname, abspath, join as pathjoin

import json

from twisted.web.resource import *;
from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource


serializer = json;

#TODO(kousu): move this out to scratch/ for reference on how to host a web socket server using AutobahnPython
class CtlProtocol(WebSocketServerProtocol):
   def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")
      
   def onMessage(self, payload, isBinary):
      if isBinary:
        print("This is probably bad. Binary message received: {} bytes.".format(len(payload)))
      else:
        print("Text message received: |{}|".format(payload.decode('utf8')))
        try:
          payload = json.loads(payload)
        except ValueError, e:
          payload = {}
 
        message = payload.get('message', 'no message :(')

        if message == 'play':
          print "play"
          poke_model.start(1)
        elif message == 'pause':
          print "pause"
          poke_model.stop()
        elif message == 'addIntervention':
          pass


   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))

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
        print("MESSAGE")
        payload = serializer.loads(payload)
        try:
          result = self._target(*payload)
          result = serializer.dumps({'result': result})
        except Exception, e:
          result = serializer.dumps({'error': str(e)}) #Security Risk?
        print("responding with", result)
        self.sendMessage(result)


def RPCEndpoint(method, debug = False):
    "why the debug param? because "
    f = WebSocketServerFactory(debug = debug, debugCodePaths = debug )
    f.setSessionParameters(externalPort = 8080) #bug in autobahn
    f.protocol = lambda: RPCProtocol(method)
    
    return WebSocketResource(f)

class RPCObjectEndpoint(Resource):
   "convenience class to make putting" #this class is feature-parable with RPCEndpoint in API #1
   "doesn't actually provide a websocket, but instead wraps each public method of o in a RPCEndpoint"
   def __init__(self, o):
      Resource.__init__(self)
      for method in (m for m in dir(o) if callable(getattr(o, m))): #find all the names (strings) of all methods
          self.putChild(method, RPCEndpoint(getattr(o, method)))


  
class Tank:
    "a class that gets its public methods exposed on a WebSocket"
    def __init__(self, weapon, (x, y, z), hp=50):
        self.weapon = weapon
        self.x = x
        self.y = y
        self.z = z
        self.hp = 50
        self.total_hp = 50
        self.heading = 33.4;
    def shoot(self):
        return "Shooting harder!"
    
    def turn(self, degrees):
        # we also have self.peer and all the other metadata that's in WebSocketServerProtocol so we can do Auth&Auth
        #, which RPCEndpoint attaches to us
        # or maybe peer comes in as a kwarg?
        # 
        self.heading+=degrees
     
    def HP(self):
        return {'current': self.hp, 'total': self.total_hp}


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    tank = Tank("Big Cannon", (55,81.1,32), 50) # somewhere in the Arctic
    
    root = File(".");
    sprites = Resource(); root.putChild("sprites", sprites)
    tank_endpoint = RPCObjectEndpoint(tank);
    sprites.putChild("tank2", tank_endpoint)
    #tank_hp_endpoint = RPCEndpoint(tank.hp);
    #tank_endpoint.put
    
    site = Site(root);
    
    reactor.listenTCP(8080, site)
   
    reactor.run()
