#!/usr/bin/python2
# the main server code
# make sure to read src/backend/README.md if this confuses you.

import sys
from os.path import dirname, abspath, join as pathjoin

import json

from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

#'working directory': not the system working directory, but the directory this program is in (so that we can be run from anywhere and find the correct assets/ folder et al.)
PROJECT_ROOT = dirname(dirname(dirname(abspath(__file__)))) #currently, the project root is two levels up from the directory the server is

#########################
## Models

# though our single model is run via python import
# in the Real System(TM) models will be dynamically
# loaded somehow, so pretend you don't see this.
from models.eutopia.eutopia import Eutopia


# NB:
# we are trying to set up a producer-consumer system, and twisted has this built in:
# https://twistedmatrix.com/documents/12.2.0/core/howto/producers.html
# ah, simpler: reactor.callLater
# useful: <https://twistedmatrix.com/documents/current/core/howto/time.html>

######################
## Twisted Components

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
          import sys
          sys.path.append('/Users/majdal-shihabi/Documents/School/4B/SYDE462_design_workshop/modex/src/backend/models')
          from eutopia.eutopia import make_magic_happen
          self.sendMessage(json.dumps(make_magic_happen()))
        elif message == 'pause':
          pass
        elif message == 'addIntervention':
          pass


   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))

class ModelDataServer(WebSocketServerProtocol):
   """
   a connection serving timeseries data from Eutopia.
   self.factory.model is Eutopia and is shared amongst
   all "Viewer" ModelDataServers.
   """
   def onOpen(self):
      self.time = self.factory.model.time #stash the time we started watching the model at
      model = self.factory.model
      def push():
          "this function essentially polls for new data"
          "using select() or events would be better"  
          if self.time < len(model.log):
              #TODO: if we are much behind where model is, do we want to batch all the updates at once?
              #  - i like it the way it is now for debugging as we get settled into the new stream, since the model and the data are running at different rates and will therefore get out of sync
              J = model.log[self.time]
              print "pushing", J, "to", self.peer #debug
              self.sendMessage(json.dumps(J))
              self.time+=1
      
      self.push = task.LoopingCall(push)
      self.push.start(0.06)


#######################
## Main

if __name__ == '__main__':
   #TODO: reindent
   debug = (len(sys.argv) > 1 and sys.argv[1] == 'debug')
   
   if debug:
      log.startLogging(sys.stdout)
   
   if debug:
     print "Starting server in", PROJECT_ROOT
   
   model = Eutopia([]) #the [] becomes model.log
   poke_model = task.LoopingCall(lambda: next(model))
   poke_model.start(4) #4 second intervals
   
   data_endpoint = WebSocketServerFactory(debug=True, debugCodePaths=True)
   data_endpoint.protocol = ModelDataServer
   data_endpoint.model = model
   
   ctl_endpoint = WebSocketServerFactory(debug=debug, debugCodePaths=True)
   ctl_endpoint.protocol = CtlProtocol
      
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
   data_resource = WebSocketResource(data_endpoint)
   ctl_resource = WebSocketResource(ctl_endpoint)
   
   root.putChild("assets", assets)  #TODO: do we prefer to have each entry in assets/ sit at the root (ie http://simulation.tld/data/ instead of http://simulation.tld/assets/data/)   
   root.putChild("ws", data_resource)    #this puts the websocket at /ws. You cannot put both the site and the websocket at the same endpoint; whichever comes last wins, in Twisted
   if debug:
     root.putChild("scratch", File(pathjoin(PROJECT_ROOT,"scratch")))
   root.putChild("ctl", ctl_resource) #this whole file is so not pythonic. Where's the D.R.Y. at, yo? --kousu
   
   #. <- /
   #./scratch <- /scratch
   #websocket <- /ws #random demo socket
   #websocket <- /ctl
   #RESTful ??
   
   ## both under one Twisted Web Site
   site = Site(root)
   data_endpoint.setSessionParameters(externalPort=8080) # hopefully unecessary soon; see https://github.com/tavendo/AutobahnPython/pull/196
   ctl_endpoint.setSessionParameters(externalPort=8080) # hopefully unecessary soon; see https://github.com/tavendo/AutobahnPython/pull/196
   reactor.listenTCP(8080, site)

   print "Now open http://127.0.0.1:8080 in your browser"
   reactor.run()

