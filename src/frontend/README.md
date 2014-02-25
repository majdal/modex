# Frontend Developer's Guide

First review the [generic developer's guide](../README.md).

As that guide suggests, get started with by starting the server:
```bash
$ python run.py
````

Once the server is up, you can mostly just leave it going and do all your work on the html, javascript, and css files here.
The server passes static files through HTTP unchanged, so you need only reload the page to see you changes as you work.

**Special WebSocket Notice Jan 26th 2014**: to see the websocket, pop open the server, load up the page, pop open the web inspector, and watch the server's output as it pushes data and data_socket.onmessage in the js console as it receives it.

## Code Structure
Code written for this project goes under src/ (so your javascripts should be src/frontend/*.js and your css under src/frontend/css/*.css).
Code dependencies (external javascripts like OpenLayers and D3), being relatively static and _not_ part of our project, are considered assets and go under assets/libs/.

## Developer's Tools

HTML5 (javascript, jquery, <canvas>, CSS3, <audio>, et al.) is a large and confoundingly ugly and stunningly elegant environment.

Get to know your browser's debug console. Use [jsFiddle](http://jsfiddle.net/) to edit code live and online, and share it with people over the internet.

Learn the limitations (mostly due to security estrictions) on what browsers can and cannot do.
The [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Same_origin_policy_for_JavaScript) is one major limitation that needs to be respected.
Browsers tend to be even more restrictive when running locally: that is, when the URL starts with "file://" instead of "http://", more rules kick in;
 Now, something (???) about these rules blocks OpenLayers from working locally in Firefox (and IE? and Opera??), but not in Chrome.
Thus in order to do any proper debugging you must launch an **http server**. Luckily, ```run.py``` spawns such a server for you.
However, if you need to test something quickly and the dense project stack is getting in your way, you can fall back on
a standard webserver.
On linux, [thttpd]() and [webfs](http://linux.bytesex.org/misc/webfs.html) are very viable options ("cd frontend; webfsd -d . & firefox localhost:8000" will get you up and hacking). ```python2 -m SimpleHTTPServer 8008``` works too.
You could also invest in learning a heavier server like
 IIS (Windows-only),
 Apache,
 nginx,
 or lighttpd,
 or [mongoose](https://code.google.com/p/mongoose)

It behooves you to have a web **developer console** open. Chrome and Firefox have built-in inspectors accessible with ctrl-shift-i,
Firefox has the option of installing the Firebug extension which is
 a) older b) better than the built in inspector.
Firefox also has the option of [Live HTTP Headers](https://addons.mozilla.org/en-US/firefox/addon/live-http-headers/)

For certain in-depth debugging scenarios like **tracking the flow of call-response** with all the headers and contents
you might need to investigate [Fiddler](http://fiddler2.com/) which is a traffic-sniffing proxy.

Another resource, useful for doing remote (ie non-LAN) debugging, is nodejs's [localtunnel](http://localtunnel.me/) service.

When developing with Chrome you should disable the cache to avoid problems. To do this open the Developer Tools (ctrl-shift-i or option+command+J), click on Settings (the gear in the top left) and then check the box marked "Disable cache (while DevTools is open)".

For testing, [Selenium](http://seleniumhq.org) is worthwhile.

## WebSockets
(see also [[../backend/README.md#WebSockets]])

Some definitions:

WAMP is the [WebSocket Application Messaging Protocol](http://wamp.ws/) and it builds __*yet another*__ protocol on top of WebSockets, which are already on top of HTTP.
WAMP provides events for websockets (which sort of seems to reintroduce what HTTP in RESTful mode gives...., (except now it's bidirectional, I guess)).
  So you can either subscribe and publish to event queues (like)
  Or you can do RPC (but if you're going to do RPC /anyway/ why bother running it over a single websocket? just make lottts of websockets. is it really that much faster?)

## D3

Dynamic d3 graphs:

* https://github.com/square/cubism (uses d3 with canvas??)
* http://www.pubnub.com/blog/create-real-time-graphs-with-pubnub-and-d3-js/

## Compatibility

Since this is a web app, it needs to be tested in all browsers on all platforms.
Since that's not a realistic goal, especially not at this stage and with this size of team,
we should at least cover:
* Firefox on Windows, Mac, and Linux
* Chrome on Windows, Mac, and Linux
