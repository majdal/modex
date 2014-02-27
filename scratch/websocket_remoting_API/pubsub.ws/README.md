pubsub.ws
=========

Pubsub should be drastically simplified so that a "topic" should be WebSocket URL.
Then "subscribing" is just connecting to that URL, and "publishing"is .send()ing to it.

Since this makes nothing that WebSocket doesn't already do, the implementation can be handled entirely server side.
The one tip to "pubsub"iness might be that if you hit the websocket address over http, it gives a note.

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
