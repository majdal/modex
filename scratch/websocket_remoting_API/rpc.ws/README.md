rpc.ws
=========

rpc.ws wraps WebSockets in a call-response style.

```
state = RPCws()

```

You might well complain that this just replaces elegant [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) with something layered over top of it for no reason, using WebSockets _should_ (fingers crossed) be much more network-efficient by dropping the HTTP headers that REST has with every request.
This essentially 
