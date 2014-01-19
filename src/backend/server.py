import sys
from os.path import dirname, abspath, join as pathjoin

#'working directory': not the system working directory, but the directory this program is in (so that we can be run from anywhere and find the correct assets/ folder et al.)
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__)))) #currently, the project root is two levels up from the directory the server is

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol

from autobahn.resource import WebSocketResource, HTTPChannelHixie76Aware
#import webbrowser

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
   
   if debug:
     print("Starting server in", PROJECT_ROOT)

   factory = WebSocketServerFactory("ws://localhost:8080",
                                    debug = debug,
                                    debugCodePaths = True)
   
   factory.protocol = EchoServerProtocol
   factory.setProtocolOptions(allowHixie76 = True) # needed if Hixie76 is to be supported
   
   webroot = pathjoin(PROJECT_ROOT,"src","frontend")
   assets = pathjoin(PROJECT_ROOT,"assets")
   if debug:
     print "putting", webroot,"at root"
     print "putting", assets,"at assets"

   ## we serve static files (most of the frontend html, js, and css) under "/" ..
   ## except for some which are under assets/
   ## and we have our WebSocket server under "/ws"
   root = File(webroot)
   assets = File(assets)  
   resource = WebSocketResource(factory)

   root.putChild("assets", assets)  #TODO: do we prefer to have each entry in assets/ sit at the root (ie http://simulation.tld/data/ instead of http://simulation.tld/assets/data/)   
   root.putChild("ws", resource)
  
   ## both under one Twisted Web Site
   site = Site(root)
   site.protocol = HTTPChannelHixie76Aware #  needed if Hixie76 is to be supported
   reactor.listenTCP(8080, site)

   #webbrowser.open('http://127.0.0.1:8080')
   print "Now open http://127.0.0.1:8080 in your browser"
   reactor.run()

