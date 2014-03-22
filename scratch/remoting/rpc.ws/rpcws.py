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
 * [ ] An DetailedRPCProtocol (and associated DetailsRPC(Object)?Endpoint calls) which is meant to cooperate with target by passing itself in so that target can do something;
     ---> or
   * [ ] or maybe a better idea is to attach the RPCProtocol object to _target, and if _target happens to be a callable class (but this
 * [ ] To simplify a common case, an AuthRPCProtocol which takes two args: an auth_manager and a target, and behaves the same as RPCProtocol except that before calling target() it checks with auth_mananger first
   ^ anyway, the problem of the leaky abstraction is going to require some cleverness to solve elegantly, but I'm sure we can get there when we need it.
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
        payload = serializer.loads(payload)
        #print getattr(self._target, "__name__","anonymous method"), "received", payload #DEBUG
        try:
          result = self._target(*payload)
          result = serializer.dumps({'result': result})
        except Exception, e:
          result = serializer.dumps({'error': str(e)}) #Security Risk?
        self.sendMessage(result)


def CallEndpoint(method, debug = False):
    "why the debug param? because "
    f = WebSocketServerFactory(debug = debug, debugCodePaths = debug )
    f.setSessionParameters(externalPort = 8080) #bug in autobahn
    f.protocol = lambda: RPCProtocol(method)
    
    return WebSocketResource(f)


class RemoteObjectEndpoint(Resource):
   "convenience class to make putting" #this class is feature-parable with RPCEndpoint in API #1
   "doesn't actually provide a websocket, but instead wraps each public method of o in a RPCEndpoint"
   def __init__(self, o):
      Resource.__init__(self)
      
      # find the names of all *public* methods
      # and bind them to rpc.ws CallEndpoints.
      for method in (m for m in dir(o) if not m.startswith("_") and callable(getattr(o, m))):
          self.putChild(method, CallEndpoint(getattr(o, method)))
