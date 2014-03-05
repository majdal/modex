wamp.ws is overengineered. There is no reason to shove that much state on top of stateless HTTP.
AutobahnPython has a solid WebSocket implementation,
but the rest of API is questionable.

These folders give proposals for replacements that can be done to simplfify.

Implementation will be done on AutobahnPython's WebSocket support.

Messaging Patterns
==================

WAMP (aka Autobahn aka crossbar.io aka Tavendo aka Tobias) sells itself as providing these features:

* PubSub
* RPC

The confounding thing is why these two very different patterns happen in the same library.

RPC provides call-response messaging, so that the client (the browser) can query the server for info
RPC is very close to the simple send()/.onmessage() pairing.
Proposal at [rpc.ws](rpc.ws).

PubSub lets you attach handlers to a stream of events. Proposal at [pubsub.ws](pubsub.ws/)

Now, in addition to these, there is a third pattern not covered by either of these, which is [state.ws](state.ws/).

Multiplexing
============

One major stumbling block that Autobahn solves
is multiplexing multiple data streams over a single websocket.

loadtest.html demonstrates that we can probably get away with just opening distinct websockets,
and that standard HTTP rules--meaning no more than [6](citation goes here) (in ye olden days [two](FIXME))
can be active per user per site at a time--do not apply. 

Still, there is some

But, instead of building a huge protocol, 
I propose to construct a websocket multiplexer, which should offer the same API as native WebSockets
but skims around the 6-connection limit.

This will require some backend support: a WebSocketProtocol that proxies to other WebSocketProtocols
In fact, if we write it in Twisted, we can probably exploit [Resource.getChild()](https://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html#getChild)
to automagically translate requests for websockets to their handlers
and not have to open up and localhost-to-localhost sockets.

The goal would be to have the multiplexer be transparent.

These codes should be 100% API-interchangable. Adding or removing the <code>M.</code> should give the same functionality, but one should be(? todo: actually write this and load-test it) faster:
<code>
w1 = WebSocket("ws://example.com/ws1")
w2 = WebSocket("ws://example.com/ws2")
w2.send("data!")
</code>

<code>
M = MultiWebSocket("ws://example.com/multiplexer")
w1 = M.WebSocket("ws://example.com/ws1")
w2 = M.WebSocket("ws://example.com/ws2")

w2.send("data!")
</code>

[SockJS](https://github.com/sockjs/websocket-multiplex) has an implementation of this.

JSON
====

Similarly, a drop-in WebSocket-compatible JSONWebSocket which autowraps and unwraps all messages to/from JSON would be useful, and probably not that long.


Relative WebSocket
==================

An apparently oversight (or purposeful lack?) is that WebSockets do not understand relative links.
This is too bad, because if we use URLs to denote simulation instances, e.g. http://example.com/games/Af354BGq/
it means that we can't write code like
<code>
$(function() {
  pieces = WebSocket("pieces/")
  pieces.onmessage = function(.....)
  //...
  chat = WebSocket("chat/")
  chat.onmessage = function(.....)
}
</code>

Instead, we would have to either:

 make a single global WebSocket endpoint and have it distinguish what
game ID ("Af354BGq") you're talking to by cookies/sessions or by you sending <code>{'session': 'Af354BGq'}</code>
<code>
$(function() {
  room = {}
  room.id = parse window.location to extract the ID
  
  pieces = WebSocket("pieces/")
  pieces.send(JSON.stringify({"session": room.id}))
  pieces.onmessage = function(.....)
  //...
  chat = WebSocket("chat/")
  pieces.send(JSON.stringify({"session": room.id}))
  chat.onmessage = function(.....)
}
</code>

or 
<code>
$(function() {
  root = parse window.location to extract the base link
  pieces = WebSocket(root + "pieces/")
  //...
  chat = WebSocket(root + "chat/")
}
</code>

kousu thinks the cleanest design either way is to have the WebSocket URLs similar to the user-facing URLs:
  so, each active room should bring up WebSocket endpoints as child Resources. So, if we wrote a RelativeWebSocket class--or even just
a wrapping constructor, in fact-- that simply did
the window.location parsing as a first step before opening the connection, but kept everything else identical,


Indexes
=======

In the demos now, there's this code:
<code>
r = Resource()
s = WebSocketResource(MyWebSocketServerFactory())

root.addChild("chatrooms", r)
r.addChild("socket", s)
</code>

It would be much more useful if it was something like this:
<code>

r = IndexingWebSocketResource()
s = WebSocketResource(MyWebSocketServerFactory())

root.addChild("chatrooms", r)
r.addChild("socket", s)
</code>

That is, where <code>r</code> is a websocket endpoint that returns a json list of all its immediate children
analogously to how plain HTTP returns (or maybe we actually ~want~ to support the plain http style; either instead of or as an addendum to the websocket style)
((if we only support websockets, you MUST use websockets to navigate the site; but if all the data is over websockets anyway, that's not that surprising))
((if we only support plain HTTP, we let spiders works but force dynamic sites to use XMLHttpRequest AND WebSocket, which is awkward because WebSocket is more or less designed to replace XMLHttpRequest))

This would allow a structure like
 *  /data <-- this is an active index page
 * /data/geo/ <-- this too
 * /data/geo/$LAYER <-- which is ..either..raster..or vector?
 *  (handling rasters is going to be tricky)
 *  (or we could do)
 *     /data/geo/vector
 *     /data/geo/raster
 *  (and the frontend/ can be hardcoded to <code>new WebSocket("data/geo/vector")</code>, assuming the relative WebSocket class is in play)




SSE
===

There's another protocol, alternate to WebSockets, that no one uses very much called **SSE**:

Some information about them:

* http://stackoverflow.com/questions/8499142/html5-server-side-event-eventsource-vs-wrapped-websocket
* http://stackoverflow.com/questions/13278365/downside-of-using-server-sent-events-for-bidirectional-client-server-communicati?rq=1

The main advantage of SSE is that it respects the same-origin policy; WebSockets do not: they can send and receive data raw to any URL hosting a websocket.
