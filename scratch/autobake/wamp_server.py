###############################################################################
##
## Partially derived from example code from:
##  Copyright (C) 2011-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import random

#from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.types import SubscribeOptions
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession


#TODO(kousu): switch to MsgPack, to compress the JSON down as far as possible
#TODO(kousu): figure out how to get the backend to receive pubsub events; do we need to make a separte ApplicationSession or something?

def favouritePolygon():
   POLYGONS = [[-1,2,-3], [44,-5,66], ["cat","mess","empty"]] # admittedly, real TopoJSON or GeoJSON polygons don't look much like this.
   return random.choice(POLYGONS)

def sumOfParrots(parrot, duck = None):
   if duck is not None:
     raise ValueError("You cannot add a parrot to a duck, that's just silly.")
   return [[parrot] + [duck]*3]*7

class PubSubComponent(ApplicationSession):
   """
   An application component that publishes events with no payload
   and with complex payloads every second.
   """

   def onConnect(self):
      self.join("realm1") # only one "realm" can be joined at a time

   @inlineCallbacks
   def onJoin(self, details):

      self.register(favouritePolygon, "favouritePolygon")
      self.register(sumOfParrots, "sumOfParrots")
      
      counter = 0
      while True:
         self.publish('lovetriangle')

         obj = {'counter': counter, 'foo': [1, 2, 3]}
         self.publish('haterhombus', random.randint(0, 100), 23, c = "Hello", d = obj)

         counter += 1
         yield sleep(1)


if __name__ == '__main__':

   import sys, argparse

   from twisted.python import log
   from twisted.internet.endpoints import serverFromString

   ## parse command line arguments
   ##
   parser = argparse.ArgumentParser()
   args = parser.parse_args()

   args.websocket = "tcp:9000"
   args.wsurl = "ws://localhost:9000"
   ## start Twisted logging to stdout
   ##
   log.startLogging(sys.stdout)

   from autobahn.twisted.choosereactor import install_reactor
   reactor = install_reactor()
   print("Running on reactor {}".format(reactor))

   ## create a WAMP router factory
   ##
   from autobahn.wamp.router import RouterFactory
   router_factory = RouterFactory()


   ## create a WAMP router session factory
   ##
   from autobahn.twisted.wamp import RouterSessionFactory
   session_factory = RouterSessionFactory(router_factory)
   
   ## [ ... ... ]
   session_factory.add(PubSubComponent())

   ## create a WAMP-over-WebSocket transport server factory
   ##
   from autobahn.twisted.websocket import WampWebSocketServerFactory
   
   # NB: args.wsurl MUST NOT INCLUDE a path; hence it is not really a URL; all it supports is protocol (which must be ws or wss), hostname, and port. anything after that gives a mysterious 
   #   File "/usr/lib/python2.7/site-packages/autobahn/websocket/protocol.py", line 3383, in setSessionParameters
   # raise Exception("path specified for server WebSocket URL")
   transport_factory = WampWebSocketServerFactory(session_factory, args.wsurl, debug = True)
   transport_factory.setProtocolOptions(failByDrop = False)

   ## start the WebSocket server from an endpoint
   ##
   server = serverFromString(reactor, args.websocket)
   server.listen(transport_factory)


   ## now enter the Twisted reactor loop
   ##
   reactor.run()
