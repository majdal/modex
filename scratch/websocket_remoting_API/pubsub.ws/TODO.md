TODO
====

* [ ] support running under AutobahnPython <= 0.7.0, where classes were autobahn.* instead of autobahn.twisted.*
* [ ] Make a demo which has the server sends 
* [ ] Make a demo where the server intervenes in the stream
* [ ] Figure out how to recognize users (WebSockets should still have access to session cookies)
  * so that the server can filter a stream depending on user; e.g. every player can subscribe to ws://minecraft.com/skyblockFBG5/blocks but they *only get* notifications on blocks within a certain radius of their avatar


* [ ] Use this code to test the intrinsic limits of WebSocket