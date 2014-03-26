Autobake: baking Autobahn into delicious 3.14159
=================================================

Minimal tests cases for [Autobahn](https://github.com/tavendo/AutobahnPython) in 
single files (which are easier to understand than the IoC-ful [examples](https://github.com/tavendo/AutobahnPython/tree/master/examples/twisted/wamp/basic)),
showing both PubSub and RPC patterns.

As Autobahn is [currently undergoing some growing pains](https://groups.google.com/d/msg/autobahnws/QagK8sDe22I/9nwHlx4I1UUJ)
the version of AutobahnJS that is known to work (0.9.0-3) is included inline here, so that if we update assets/libs/autobahn.js and suddenly find a regression we can at least compare agains a known working instance.


Files Here
==========

`autobahn.js` is AutobhanJS version 0.9.0-3.

## autobah

`autobah.js` and `autobah.py` were minimal test cases of the weird need Autobahn had for you to tell it what its address was (a requirement Twisted is supposed to handle).
Fixed in [594066](https://github.com/tavendo/AutobahnPython/commit/5940660d9b29f1c7a4c3fc76e09f6002927c2dde) and [2b1648](https://github.com/tavendo/AutobahnPython/commit/2b16489aa1f1403bee6dd597bd8dfa542b2dca05) because [we nagged him about it](https://github.com/tavendo/AutobahnPython/pull/196)

## wamp

`wamp_client.html` and `wamp_server.py` demonstrate (against AutobahnPython 0.8.1 and AutobahnJS 0.???) how to use the [WAMP](http://wamp.ws) protocol.
They're gaudy.


Secrets and Tricks
==================

`WebSocketServerFactory` has two undocumented kwargs that it will take: `debug` and `debugCodePaths`.
[Straight from the man himself](https://groups.google.com/d/msg/autobahnws/E37ZIwEYnUg/iI_W4hVyRHMJ),
set to true, they make the server log packet-level details about what it's doing to the Twisted log
 ((use `twisted.python.log.startLogging(sys.stdout)` to make visible)), which can be useful if
  you suspect a bug in Autobahn, Chrome, or Firefox. (You could also just use Wireshark).

