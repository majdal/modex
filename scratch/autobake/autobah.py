"""
minimal test case for removing dependency on WebSocketServerProtocol.setSessionParams()

"""

import sys

from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource


class EchoProtocol(WebSocketServerProtocol):
   def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")
      
   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {} bytes".format(len(payload)))
      else:
         print("Text message received: |{}|".format(payload.decode('utf8')))

      self.sendMessage(payload*2, isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))


if __name__ == '__main__':
   log.startLogging(sys.stdout)
   
   # all these three are equivalent under AutobahnPython 0.8.5
   #ws_echo_endpoint = WebSocketServerFactory("ws://localhost:8080", debug=True, debugCodePaths=True)
   #ws_echo_endpoint = WebSocketServerFactory("ws://:8080", debug=True, debugCodePaths=True)
   #ws_echo_endpoint = WebSocketServerFactory(externalPort=8080, debug=True, debugCodePaths=True)
   # this one is not:
   ws_echo_endpoint = WebSocketServerFactory(debug=True, debugCodePaths=True)
   
   ws_echo_endpoint.protocol = EchoProtocol
   
   root = File(".")
   ws_echo_resource = WebSocketResource(ws_echo_endpoint)
   root.putChild("echo", ws_echo_resource)
   
   site = Site(root)
   reactor.listenTCP(8080, site)
   
   print "Now open http://127.0.0.1:8080 in your browser"
   reactor.run()

