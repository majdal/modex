rpc.ws
=========

rpc.ws wraps WebSocket's message-based protocol into a call-response protocol plus automatic `json` serialization, with _promises_ for interacting with return values.

```
// open communication sockets
open_fridge = RPCws.Call("ws://example.com/open_fridge")
close_fridge = RPCws.Call("ws://example.com/close_fridge")
get_temperature = RPCws.Call("ws://example.com/get_temperature")

// ... 

// use one of them:
open_fridge(Kitchen.FAST).then(function(door) {
  console.log("Fridge door opened! It is now,", door.damage);
}).fail(function(error) {
  console.error("Unable to get to the tasties:", error)
})
```


It also supports (but wrapping several `RPCws.Call` objects together), exposing the methods on an entire object. In a large system with lots of architecture, you're probably going to favour exposing whole objects at once:
```
cookie = RPCws.RemoteObject("ws://example.com/cookiejar/cookie1", ["chips", "size"])
cookie.chips("vanilla").then(function(vanilla_chips) {
  vanilla_chips.forEach(function(chip) {
    console.log("Nom nom", chip);
    })
})
```

`ayepromise` provides our [promises](http://promisesaplus.com/implementations) which then provide the `.then()` and `.fail()` methods. This requires a change in thinking about how to program: RPC is fundamentally a long-running network phenomenom, and need to design your application asynchronously. If you're used to javascript, you're probably already used to this. If you're not, read the promises documentation and learn the full power of it.

Since serialization is `json`-based you are restricted to sending only relatively simple datastructures. Sineand the front and backend are dynamic languages, these calls are fairly weakly typed. You should know what your frontend and backend are sending. You will get an error at runtime if you call them wrong:
```
cookie.chips("vanilla", Math.PI).then(function(vanilla_chips) {
  vanilla_chips.forEach(function(chip) {
    console.log("Nom nom", chip.radius); //error: chip.radius is undefined
    })
}).fail(function(error) {
  console.error(error); // --> 'type error somethingsomethingsomething XXX FIXME'
})
```

By itself, an rpc session only talks to one method and one method only. This means that URLs are methods and methods are URLs, REST-style, but without all the overhead of sending HTTP headers every message. However, if you have a lot of active objects and methods you _will_ use a lot of active sockets. But if you use `multiplex.ws` (**NOT WRITTEN YET**), which provides something like HTTP-keepalive but for WebSockets, you can avoid that (_TODO: write `multiplex.ws` and make a convenience flag on RPCws.RemoteObject which internally assumes the RemoteObject URL is a multiplex.ws endpoint and that the methods on the object are to be multiplexed across_); if you open one socket per object, you can use your packet insepctors to track when objects are being talked to.


The protocol is currently only implemented in javascript (frontend) and Python-Twisted-AutobahnPython (backend) right now but there's no reason (with enough tests as a safety net) it couldn't be on Python-`asyncio`-AutobahnPython or in nodejs or in something else as well.


For a related pattern, see `pubsub.ws`.

Demo
====

Assuming you have `python` and `nodejs` installed, in one terminal, run
```
$ python2 tankrpc.py
```

and then in another run
```
$ node tankrpc.js
```

You should see.
