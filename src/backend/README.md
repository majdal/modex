# Backend Developer's Guide

First review the [generic developer's guide](../README.md).

As a backend developer, it is worthwhile to learn how to run the server directly.
While you can develop portions of it under a simple ```run.py```,
running it directly removes the source of potential bugs from that one layer of indirection
 and lets you tweak command line arguments. To run the server directly, use:
```bash
$ python src/backend/server.py
```

It doesn't matter what folder you run the server from (_if it does seem to matter, file a bug report_)
```bash
$ cd src/backend
$ python server.py
```

If you add 'debug' as an argument to the server you will see the web logs:
```bash
$ cd src/backend
$ python server.py debug
2014-01-19 16:20:19-0500 [-] Log opened.
2014-01-19 16:20:19-0500 [-] Site starting on 8080
2014-01-19 16:20:19-0500 [-] Starting factory <twisted.web.server.Site instance at 0x2e4e680>
2014-01-19 16:20:19-0500 [-] Now open http://127.0.0.1:8080 in your browser
2014-01-19 16:20:20-0500 [HTTPChannelHixie76Aware,0,127.0.0.1] 127.0.0.1 - - [19/Jan/2014:21:20:20 +0000] "GET /assets/ HTTP/1.1" 404 145 "-" "Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0"
^C2014-01-19 16:20:25-0500 [-] Received SIGINT, shutting down.
2014-01-19 16:20:25-0500 [twisted.web.server.Site] (TCP Port 8080 Closed)
2014-01-19 16:20:25-0500 [twisted.web.server.Site] Stopping factory <twisted.web.server.Site instance at 0x2e4e680>
2014-01-19 16:20:25-0500 [-] Main loop terminated.
```

 (coming soon: extra arguments taking filenames of datalayers to load up)

## Developer's Tools

????

## WebSocket Notes

We're using [autobahn](https://github.com/tavendo/AutobahnPython) as our backend implementation of the websocket protocol (it's a protocol that rides on top of HTTP, just to make the web stack even deeper).
WebSockets provide a (**TODO**: summarize and/or link why websockets) more efficient protocol--less bandwidth and much better latency--than typical request-response HTTP. We are using them because we expect (though we don't actually have any)

* [Server-side WebSocket API reference](https://github.com/tavendo/AutobahnPython/tree/master/doc)
* [Browser-side WebSocket API reference](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket).

WebSockets, like the _webservice_ protocols that came before them, are referenced like any other HTTP or object: with a URL.
A websocket URL looks like "ws://server:port/path/to/endpoint" or "wss://server:port/path/to/endpoint", the difference being that the latter causes the websocket to connect over SSL.

Autobahn is functional, but it's [website](http://autobahn.ws/python/tutorials/echo/) is currently (**TODO**: update this when this changes) out of date. The github docs and examples seem to be reasonably up to date (they have test cases and stuff, so they better be) so for now, use that as your reference.

Here's some guidance on debugging websockets. Debugging them means tweaking things in ```server.py``` and then opening up
a javascript console from a browser. These notes are in this **README** and not **[[../frontend/README.md]]** since this is really more of an issue--but both sides can and should refer and add to these notes.

When you're in the browser console, you can make a websocket to test with by:
```
   ws = new WebSocket("ws://server:9000/endpoint");
```
   If you drop the ```new``, it'll still work. The difference [is](http://trephine.org/t/index.php?title=Understanding_the_JavaScript_new_keyword) and [occasionally non-existent](

Using 'wss' is a good idea, but unless you've got SSL set up on the server it'll hang and you won't know why because neither the browser API nor Autobahn explicitly mention "SSL" when such a connection fails.

The hostname MUST be the same as the site you are on due to the same-origin policy (unless you do some server side black magic which we shall avoid)
 * In particular, when debugging, you should first open up the server in your webbrowser (autobahn gives a useful response if you hit it with http:// instead of ws://, so if your websocket is supposed to be ws://localhost:9242/ws, then first open http://localhost:9242/ws before trying to debug stuff)

This one-liner lets you test if a websocket is listening:
 ```
  s = new WebSocket("ws://localhost:8080"); s.onmessage = function(d) { console.log("recv: " + d.data); }; setTimeout(function() { s.send("butts")},1000);
```
  (the setTimeout is because the websocket needs a moment to wake up and handshake; better would be 'onopen'... but with this method you get an error instead of a silent an inexplicable hang)

## Gotchas




You must run the server under python2. Twisted is [the largest](https://wiki.python.org/moin/Python2orPython3) library yet to be ported to python3.

In twisted, node.putChild() must have its first argument **NOT** end with a '/'. That will cause mysterious 404s with no clue in the log.

In OL3, when loading Vector layers, you (for some currently unknown reason) must pass 'renderer: ol.RendererHint.CANVAS' to the Map constructor or else they will fail with a nil ptr exception in the bowels of OL.


## Compatibility

we should at least cover:
Installing the server on
* Ubuntu
* Mac
