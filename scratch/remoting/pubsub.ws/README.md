pubsub.ws
=========

WebSocket PubSub can be drastically simplified over [the competition](http://wamp.ws/faq/#pubsub)
so that there is no need for a [new protocol](https://github.com/tavendo/WAMP/blob/master/spec/advanced.md).
Simply equate "topics" with URLs; then "subscribing" is connecting and "publishing" is sending.

Since this uses nothing that WebSocket doesn't already do, the implementation can be handled entirely server side, making the client side code dead simple:

Examples
========

A simple server feed:
```
temperature_subscription = WebSocket("ws://example.com/feeds/sensors/temperature")
temperature_subscription.onmessage = function(evt) {
  console.log("Temp is ", evt.data['t'])
}

```


A simple room (see [chat.html](chat.html) for the working example):
```
channel = WebSocket("ws://example.com/chatrooms/ireland/")
channel.onmessage = function(evt) {
   evt.data = JSON.parse(evt.data)
   $("#chatwindow").val(evt.data['nickname'] + ": " + evt.data['message'])
}
inputbox = $("#inputbox")
inputbox.click(function() { 
  channel.send(inputbox.content)
  inputbox.content = null;
})
```

(no server example yet, since there's literally nothing interesting in the server yet)


Tips and Tricks
===============

In true RESTful fashion, this gimmick forces every single pubsub endpoint to be unique.
So if you want to have some sort of sessioning going on, like different instances of a games,
you must arrange 
You can do this in Twisted with something like

```
roomid = uuid.uuid4().hex
site.putchild(roomid, roomroot
roomroot = twisted.web.resource.Resource()
roomroot.putchild("event1", PubSubBroker())  #actually this is wrong, because Autobahn insists on knowing 
roomroot.putchild("event2", PubSubBroker())  #WebSocket URLs twice over
roomroot.putChild("images", otherinterestingHTTPresource())
send_roomid_somewhere_useful_so_the_users_can_join(roomid)

```

Since this just uses the plain WebSocket API, it is agnostic about serialization. You can use JSON, msgpack, plain string buffers, or anything else.
You will need to implement handling of that yourself, but the flexibility to use different types for different data without the overhead of headers is worth it.

Missing Pieces
==============

As of this commit, this file does not support a thoughtful server. The server has no means to influence messages it relays.
That can change, but it will require some API design considerations.

See [TODO](TODO.md) for gorey details.
