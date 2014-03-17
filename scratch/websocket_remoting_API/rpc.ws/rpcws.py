"""
RPC.ws: python server code

This on AutobahnPython on Twisted.

Provides one class:
 - RPCProtocol, which wraps a callable into something that speaks websockets+json

And two convenience functions, which make Twisted Resource objects:
 - RPCEndpoint - which turns an RPCProtocol into something usable
 - RPCObjectEndpoint - which wraps all public methods on an object into RPCEndpoints

TODO:
 * [ ] figure out a sane way for users to change the serializer
 * [ ]
"""

import json

from twisted.web.resource import *;

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

serializer = json;

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
