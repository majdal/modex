rpc.ws
=========

rpc.ws wraps WebSocket's message-based protocol into a call-response protocol plus automatic `json` serialization, with _promises_ for interacting with return values.

Once you set up some CallEndpoints on the backend, interacting with them is short and sweet:
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

// Clean up and shut down connections
// (this isn't really necessary; if you don't do this you'll see
// server errors about dropped connections, but Calls() won't care
open_fridge.close()
close_fridge.close()
get_temperature.close()
```

You can send any number of calls simultaneously. 
They will be serialized to the underlying WebSocket
stream in the order they were called and they will resolve in that order (_FIFO queue_).
```
TODO: example of this.
 (for now, see tankrpc.js)
```

It also supports (by wrapping several `RPCws.Call` objects together), exposing the public methods of an entire object.
In a large system with lots of architecture, you're probably going to favour using `rpc.ws` like this:
```
cookie = RPCws.RemoteObject("ws://example.com/cookiejar/cookie1", ["chips", "size"])

cookie.ready(function() {
  // once the connection comes up
  // eat some chocolate chips every 9.75 seconds
  setInterval(function() {
    cookie.chips("vanilla").then(function(vanilla_chips) {
      vanilla_chips.forEach(function(chip) {
        console.log("Nom nom", chip);
      })
    })
  }, 9750)
})
```

`ayepromise` provides our [promises](http://promisesaplus.com/implementations) which then provide the `.then()` and `.fail()` methods. This requires a change in thinking about how to program: RPC is fundamentally a long-running network phenomenom, and need to design your application asynchronously. If you're used to javascript, you're probably already used to this. If you're not, read the promises documentation and learn the full power of it.

Since serialization is `json`-based you are restricted to sending only relatively simple datastructures. Since front and backend are in dynamic languages and this is a very thin wrapper on top of those, these calls are weakly typed and you will. You should know what your frontend and backend are sending. You will get an error at runtime if you call them wrong:
```
cookie.chips("vanilla", Math.PI).then(function(vanilla_chips) {
  vanilla_chips.forEach(function(chip) {
    console.log("Nom nom", chip.radius); //error: chip.radius is undefined
    })
}).fail(function(error) { // --> will give a stringified Python exception to your javascript code:
  console.error(error);   // error: 'chips() takes exactly 2 arguments (3 given)' 
})
```

By itself, an rpc session only talks to one method and one method only. This means that URLs are methods and methods are URLs, REST-style, but without all the overhead of sending HTTP headers every message. However, if you have a lot of active objects and methods you _will_ use a lot of active sockets. But if you use `multiplex.ws` (**NOT WRITTEN YET**).

The protocol is currently only implemented in javascript (frontend) and Python-Twisted-AutobahnPython (backend) right now but there's no reason (with enough tests as a safety net) it couldn't be on Python-`asyncio`-AutobahnPython or in nodejs or in something else as well.


For a different sort of communication pattern, not based on calls and responses, see `pubsub.ws`.
For a different sort of data sync pattern, which hides the irrelevant messaging parts, see `state.ws`.

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

You should see (maybe reordered a bit for random network delays):
```
$ node tankrpc.js
done Tank demo initialization;
tank sockets opened; calling
1st call: Tank2's hp: 50 / 50
successfully rotated the tank; server returned: null
tank.turn() failed, as expected: turn() takes exactly 2 arguments (1 given)
2nd: Tank2's hp: 50 / 50
Shutting down Tank connections

/home/kousu/School/WICI/sig/repos/modex/scratch/remoting/rpc.ws/rpcws.js:157
	      throw new Error("WebSocket not open")
	            ^
Error: WebSocket not open
    at RemoteObject.call [as HP] (/home/kousu/School/WICI/sig/repos/modex/scratch/remoting/rpc.ws/rpcws.js:157:14)
    at null._onTimeout (/home/kousu/School/WICI/sig/repos/modex/scratch/remoting/rpc.ws/tankrpc.js:28:8)
    at Timer.listOnTimeout [as ontimeout] (timers.js:110:15)

```
The error is expected, and demonstrates that we know better than to try to send data to a closed socket.


TODO
=====

* Make Calls and RemoteObjects `then()able`? Instead of `.ready()` we could use `.then()`, and if the connection fails (`ws.onerror`) we can pass that out too.
  * Do WebSockets conform to the _promises_ spec? Like, do they _guarantee_ to only .onerror() and .onopen() and .onclose() at most ONCE each?
* Scrap the error checking in rpcws.js? There's something to be said for thinner wrapping; relying on the built in errors will make people understand that they are actually using WebSockets.
* Make it easier to fake _realms_: make convenience methods to set up identical CallEndpoint trees under subpaths, e.g. so that `ws://example.com/games/session04g78a4B/` and `ws://example.com/games/session99g77a23/` both contain *disinct* objects/methods `players/`, `pieces/`, `board/` etc, and make a `RelativeWebSocket` js class which papers over the detail of which session you're talking to.
* Some way of changing decisions based on client ("`.peer`", in Autobahn terminology) identity (ip address/cookies/http login/etc).
  * One idea: configurable server-side redirection of clients to different CallEndpoints. This could be done: 
    * _openly_, with a `HTTP 302` (or another 3xx code), or
    * _internally_, by setting up a proxy object.
    * Simple use case (which fits the _openly_ method): if we know alice@attacker.com is supposed to be in `/chatsessions/hackme` (eg say her computer dropped off the net and reconnected) then we can use a 302 `/chatsessions/ -> /chatsessions/hackme` to send her over.
    * Complicated use case (which fits the _internally_ method): users only have access to a particular subportion of a spreadsheet, according to what the team has shared with them. So the `spreadsheet.rows` call that the `CallEndpoint` wraps needs to behave differently depending on the user.
      * We could figure out some way to pass `.rows` the `.peer` information (kwargs? some sort of global?), or
      * Create (with the Factory pattern) a new `spreadsheet` object for each user that takes `.peer` in its constructor.
* `multiplex.ws` which provides something like HTTP-keepalive but for WebSockets. you can avoid that
  * make a flag on RPCws.RemoteObject that makes it assumes the RemoteObject URL is a multiplex.ws endpoint instead of opening direct WebSocket connections everywhere
  *  (in fact, right now, RPCObjectEndpoint is just a `Resource`; we could trivially make it a `MultiplexingWebsocketResource` and make this the default?)
  * This way--if you open one socket per object--you can balance the benefits of multiplexing use your packet insepctors to track when objects are being talked to.
