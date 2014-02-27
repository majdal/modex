
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

One major stumbling block that Autobahn does (or should be--we don't actually have performance numbers yet) solve
is multiplexing multiple data streams over a single websocket. AFAIK, every WebSocket means one TCP connection,
which if standard HTTP rules apply, means no more than [6](citation goes here) (in ye olden days [two](FIXME))
can be active per user per site at a time.

But, instead of building a huge protocol, 
I propose to construct a websocket multiplexer, which should offer the same API as native WebSockets but skims around the 6-connection limit.
