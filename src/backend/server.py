#!/usr/bin/python2
# the main server code
# make sure to read src/backend/README.md if this confuses you.

import sys
from os.path import dirname, abspath, join as pathjoin

#'working directory': not the system working directory, but the directory this program is in (so that we can be run from anywhere and find the correct assets/ folder et al.)
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__)))) #currently, the project root is two levels up from the directory the server is

from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

import autobahn

# autobahn changed their API between (which happens to be within the last month of so as of this commit)
# they added asyncio (which is py3.4-native) as an alternate option to twisted (which is py2-native),
# and hence moved moved classes from autobahn.* to autobahn.twisted.*
# evidence:
#  https://raw.github.com/tavendo/AutobahnPython/v0.7.0/examples/twisted/websocket/echo/server.py
#   ~~ the change happened here, now  ~~
#  https://raw.github.com/tavendo/AutobahnPython/v0.6.5/examples/websocket/echo/server.py
#  https://raw.github.com/tavendo/AutobahnPython/v0.6.4/examples/websocket/echo/server.py
#  https://raw.github.com/tavendo/AutobahnPython/v0.5.14/examples/websocket/echo/server.py
#  https://raw.github.com/tavendo/AutobahnPython/e1dae070e67a9361f14beba775c66961e06d43ff/demo/echo/echo_server.py

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, HTTPChannelHixie76Aware

#TODO: import gdal and take vector layers to load as arguments
#TODO: Autobahn as of 0.7.4 actually supports py3, even though Twisted doesn't; this might be worth investigating.

import json

data = {'Incandescent': [-_ for _ in range(10)],
                'CFL': [_ for _ in range(10)],
                'Halogen': [_*2 for _ in range(10)],
                'LED': [_*0.5 for _ in range(10)],
        }


# we are trying to set up a producer-consumer system, and twisted has this built in:
# https://twistedmatrix.com/documents/12.2.0/core/howto/producers.html
# ah, simpler: reactor.callLater

import csv

class JsonDataServer(WebSocketServerProtocol):
   def onConnect(self, request):
      print("Client connecting: {}".format(request.peer))

   def onOpen(self):
      print("WebSocket connection open.")
      
      #I want to speak dynamically: so, as data comes in, push it to the client
      # but I don't see how to do this?? what thread am I running on???
      # ah!
      dat = pathjoin(PROJECT_ROOT, "assets/data/static_lightbulbs.tsv")
      dat = open(dat)
      dat = csv.reader(dat, dialect=csv.excel_tab)
      header = next(dat)
      print("read header:", header)
      
      # this
      def feed():  #a coroutine, meant to be pumped by the twisted event loop
        for row in dat:
          J = dict(zip(header, row))
          print "pushing", J, "to the client"
          self.speak(J)
          yield
      g = feed()
      def loop():  #wrap the coroutine (there's probably a cleaner way to do this, but shh)
        try:
          next(g)
          reactor.callLater(3, loop)
        except StopIteration:
          pass
      loop()  #kick it off

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {} bytes".format(len(payload)))
      else:
         print("Text message received: |{}|".format(payload.decode('utf8')))

      #self.sendMessage(json.dumps(data), isBinary)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))
   
   def speak(self, o):
     "send object o across the wire to the listener"
     "the idea is that in our setup, the clients mostly listen to us"
     if not isinstance(o, dict): #coerce 
       o = o.__dict__ #security risk?
     self.sendMessage(json.dumps(o), False)
      

#def WebSocket( #can i wrap it to be les stupid?

if __name__ == '__main__':

   if len(sys.argv) > 1 and sys.argv[1] == 'debug':
      log.startLogging(sys.stdout)
      debug = True
   else:
      debug = False
   
   if debug:
     print "Starting server in", PROJECT_ROOT

   factory = WebSocketServerFactory("ws://localhost:8080",
                                    debug = debug,
                                    debugCodePaths = True)
   factory.protocol = JsonDataServer
   #factory.setProtocolOptions(allowHixie76 = True) # needed if Hixie76 is to be supported   

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
   root.putChild("ws", resource)    #this puts the websocket at /ws. You cannot put both the site and the websocket at the same endpoint; whichever comes last wins, in Twisted
  
   ## both under one Twisted Web Site
   site = Site(root)
   #site.protocol = HTTPChannelHixie76Aware #  needed if Hixie76 is to be supported
   reactor.listenTCP(8080, site)

   print "Now open http://127.0.0.1:8080 in your browser"
   reactor.run()

