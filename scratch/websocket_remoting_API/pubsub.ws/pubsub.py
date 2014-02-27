# pubsub.py
# kousu, Feb 2014
# 2-clause BSD
"""
Implements a publish-subscribe (PubSub) broker over WebSockets.

Each subscribable "topic" is just a URL. Messages are "published" by sending websocket messages,
and are relayed, unfiltered, to every other websocket open to the same endpoint. The server can publish messages by calling

If you need filtering or anything else fancier, subclass this.

Since we're using WebSockets in Python, we're using Autobahn on Twisted, so make sure those are installed

"""

#TODO(kousu): support old Autobahn (the only change should be an exception handler around the imports to try importing the old paths
#TODO(kousu): figure out how to peg messages to users

import sys

from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.python import log

import autobahn.twisted.websocket
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource



class PubSubProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))
    
    def onOpen(self):
        print("WebSocket connection open.")
    
    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: |{}|".format(payload.decode('utf8')))
    
      #self.sendMessage(json.dumps(data), isBinary)
    
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

class WebSocketServerFactory(autobahn.twisted.websocket.WebSocketServerFactory, object): pass #hack around python2

class PubSubBroker(WebSocketServerFactory):
    protocol = PubSubProtocol
    def __init__(self, *args, **kwargs):
        super(PubSubBroker, self).__init__(*args, **kwargs)


if __name__ == "__main__":
    
    log.startLogging(sys.stdout)
    broker = PubSubBroker("ws://localhost:8080", debug = True, debugCodePaths = True)
    # it is a wart that PubSubBroker needs to know the URL it comes up on
    root = File(".")
    chatrooms = Resource()
    root.putChild("chatrooms", chatrooms)
    chatrooms.putChild("ireland", WebSocketResource(broker))
    
    reactor.listenTCP(8080, Site(root))
    reactor.run()
