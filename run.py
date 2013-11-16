import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol

from autobahn.resource import WebSocketResource, HTTPChannelHixie76Aware


class EchoServerProtocol(WebSocketServerProtocol):

   def onMessage(self, msg, binary):
      self.sendMessage(msg)


if __name__ == '__main__':

   if len(sys.argv) > 1 and sys.argv[1] == 'debug':
      log.startLogging(sys.stdout)
      debug = True
   else:
      debug = False

   factory = WebSocketServerFactory("ws://localhost:8080",
                                    debug = debug,
                                    debugCodePaths = debug)

   factory.protocol = EchoServerProtocol
   factory.setProtocolOptions(allowHixie76 = True) # needed if Hixie76 is to be supported

   resource = WebSocketResource(factory)

   ## we server static files under "/" ..
   root = File(".")
   src = File("src")
   lib = File("lib")
   ## and our WebSocket server under "/ws"
   root.putChild("ws", resource)
   root.putChild("src", src)
   root.putChild("lib", lib)

   ## both under one Twisted Web Site
   site = Site(root)
   site.protocol = HTTPChannelHixie76Aware # needed if Hixie76 is to be supported
   reactor.listenTCP(8080, site)

   reactor.run()