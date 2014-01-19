import sys

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol

from autobahn.resource import WebSocketResource, HTTPChannelHixie76Aware
import webbrowser

import json

class EchoServerProtocol(WebSocketServerProtocol):

    def onMessage(self, msg, binary):
        data = {'Incandescent': [-_ for _ in range(10)],
                'CFL': [_ for _ in range(10)],
                'Halogen': [_*2 for _ in range(10)],
                'LED': [_*0.5 for _ in range(10)],
        }
        #import ipdb; ipdb.set_trace()
        self.sendMessage(json.dumps(data))


if __name__ == '__main__':

   if len(sys.argv) > 1 and sys.argv[1] == 'debug':
      log.startLogging(sys.stdout)
      debug = True
   else:
      debug = False

   factory = WebSocketServerFactory("ws://localhost:8080",
                                    debug = debug,
                                    debugCodePaths = True)

   factory.protocol = EchoServerProtocol
   factory.setProtocolOptions(allowHixie76 = True) # needed if Hixie76 is to be supported

   resource = WebSocketResource(factory)

   ## we server static files under "/" ..
   root = File(".")
   ## and our WebSocket server under "/ws"
   root.putChild("ws", resource)

   ## both under one Twisted Web Site
   site = Site(root)
   site.protocol = HTTPChannelHixie76Aware # needed if Hixie76 is to be supported
   reactor.listenTCP(8080, site)

   webbrowser.open('http://127.0.0.1:8080')
   reactor.run()