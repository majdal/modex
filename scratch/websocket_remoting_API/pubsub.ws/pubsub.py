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
    """
    Handle talking to a single web
    The way this works is by cooperating with PubSubBroker, which is meant to be this class's Twisted Factory
    Everytime a connection opens or gets a message, this class notifies its Factory, which represents the particular endpoint (aka URL (aka topic, in the pubsub abstraction))
    and in turn its factory has a queue of messages to send to instances of this class
    """
    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))
    
    def onOpen(self):
        print("WebSocket connection open.")
        self.factory._listeners.append(self)
    
    def onMessage(self, payload, isBinary):
        self.factory.send(payload, isBinary)
        if isBinary:
            print("Binary message received: {} bytes".format(len(payload)))
        else:
            print("Text message received: |{}|".format(payload.decode('utf8')))
    
      #self.sendMessage(json.dumps(data), isBinary)
    
    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {}".format(reason))
        self.factory._listeners.remove(self)


class PubSubBroker(WebSocketServerFactory):
    """
    a publish-subscribe message broker,
    implemented as a Twisted factory for websockets
    """
    protocol = PubSubProtocol
    def __init__(self, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs) #can't use super(); twisted and autobahn do not derive their classes from `object`
        self._listeners = []
    
    def send(self, payload, isBinary):
        "enqueue a message to send to all listener -- but don't actually send it yet"
        "payload must be a str or a unicode"
        print "relaying", payload, "to", len(self._listeners), "clients"
        for lsnr in self._listeners: #iterate over all PubSubProtocols that have attached to this "topic"
            reactor.callLater(0, lsnr.sendMessage, payload, isBinary)  #XXX is it okay to use reactor here??


class PubSubResource(WebSocketResource):
    """
    convenience class so you can say
      site.putChild("path", PubSubResource())
    """
    def __init__(self, url):
        WebSocketResource.__init__(self, PubSubBroker(url, debug = True, debugCodePaths = True))

if __name__ == "__main__":
    
    log.startLogging(sys.stdout)

    root = File(".")
    chatrooms = Resource()
    root.putChild("chatrooms", chatrooms)
    chatrooms.putChild("ireland", PubSubResource("ws://localhost:8080")) # it is a wart of Autobahn that
                                                                         # PubSubBroker needs to know its URL
    
    reactor.listenTCP(8080, Site(root))
    reactor.run()
