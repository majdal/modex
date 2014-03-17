

import sys
from os.path import dirname, abspath, join as pathjoin

import json

from twisted.web.resource import *;
from twisted.internet import reactor
from twisted.internet import task
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource

from rpcws import *
  
class Tank:
    "a class that gets its public methods exposed on a WebSocket"
    def __init__(self, weapon, (x, y, z), hp=50):
        self.weapon = weapon
        self.x = x
        self.y = y
        self.z = z
        self.hp = 50
        self.total_hp = 50
        self.heading = 33.4;
    def shoot(self):
        return "Shooting harder!"
    
    def turn(self, degrees):
        # we also have self.peer and all the other metadata that's in WebSocketServerProtocol so we can do Auth&Auth
        #, which RPCEndpoint attaches to us
        # or maybe peer comes in as a kwarg?
        # 
        self.heading+=degrees
     
    def HP(self):
        return {'current': self.hp, 'total': self.total_hp}


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    
    tank = Tank("Big Cannon", (55,81.1,32), 50) # somewhere in the Arctic
    
    root = File(".");
    sprites = Resource(); root.putChild("sprites", sprites)
    tank_endpoint = RPCObjectEndpoint(tank);
    sprites.putChild("tank2", tank_endpoint)
    #tank_hp_endpoint = RPCEndpoint(tank.hp);
    #tank_endpoint.put
    
    site = Site(root);
    
    reactor.listenTCP(8080, site)
   
    reactor.run()
