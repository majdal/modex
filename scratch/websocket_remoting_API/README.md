wamp.ws is overengineered. There is no reason to shove that much state on top of stateless HTTP.
AutobahnPython has a solid WebSocket implementation,
but the rest of API is questionable.

These folders give proposals for replacements that can be done to simplfify.

Implementation will be done on AutobahnPython's WebSocket support.
(note: there's [other options](../../wiki/Platforms-and-APIs.md#networking))

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


(
[SockJS](https://github.com/sockjs/websocket-multiplex) has an implementation of this; they've done it reasonably cleanly on top of Twisted+their own Twisted-WebSocket implementation, and indeed have done just what I thought they'd have to: designed a small protocol ([it consists](https://github.com/sockjs/websocket-multiplex/blob/master/multiplex_client.js) of wrapping "data" in "sub,channel" to subscribe, "msg,channel,data" to send data, and "uns,channel" for detaching) and written client-side and server-side implementations of it. On the backend the multiplexer simply redirects messages transparently to WebSocketProtocols
```
multiplex.addFactory("channel1", Factory.forProtocol(EchoProtocol))
multiplex.addFactory("channel2", Factory.forProtocol(ChatProtocol))
```
and even has provisions (via subclassing) for dynamic channel (aka topic aka endpoint) creation.

which is much cleaner than in Autobahn where to run multiple streams over a single channel you need to change how you write your code:
```
#....
# suppose we have jumped through the hoops neessary to construct an ApplicationSession object; call it multiplex

# you /could/ do this, but this gives no way to react, because ~you aren't a websocket~
multiplex.subscribe(echo_handler, "channel1") 
multiplex.subscribe(chat_handler, "channel2") 

# ...

# to respond, you need to
# a) shove unrelated code (echo_handler and chat_handler) into the same class, or abuse python's dynamicness
# b) hard-code the channel names (because you must know where to publish to; that isn't hidden in your class)
class Multiplex2(ApplicationSession):
  #...
  def __init__(self):
     self.subscribe(self.echo_handler, "channel1")
     self.subscribe(self.chat_handler, "channel2")
  def echo_handler(self, *data):
     self.publish("channel1", data)
#....
```

SockJS-Multiplex has no security, and clients can cause servers to (un)subscribe (from)to channels and vice-versa. That might be a feature.
Its rationale is [in a enthusiastic but concise blog post](https://www.rabbitmq.com/blog/2012/02/23/how-to-compose-apps-using-websockets/), wherein it sounds like all of their concerns are my concerns: resuability, composability, simplicity. **The one thing we need to check out before diving into SockJS is whether we can take their server-side multiplexer and drop it on top of Autobahn; if they've really done it cleanly then there should be no trouble doing that --- actually, SockJS-Multiplex isn't implemented in twisted yet; we can maybe snitch their protocol though and implement it our way)

One nit though: in my design, I want the multiplexing to be totally transparent: every channel (aka topic) should be a ws:// URL and there should be no channels open that you couldn't open directly. SockJS-multiplex hangs arbitrary-name channels off their pubsub protocol. --it might be tricky determining which URL corresponds to which node, but I think we can do it, and then we have a SINGLE namespace instead of hiding.
)

JSON
====

Similarly, a drop-in WebSocket-compatible JSONWebSocket which autowraps and unwraps all messages to/from JSON would be useful, and probably not that long.


Security
========

We need to think about implementing authentication (we can use cookies, so long as they are the magic non-pinnable session cookies; if we do it right then authors can plug in any of the authentication modules twisted can do) and we need to implement flood-control (XXX does crossbar.io do this?)

What exactly this means is unclear. Maybe instead of bringing up a WebSocketResource we bring up a GuardingWebSocketResource?


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
  
