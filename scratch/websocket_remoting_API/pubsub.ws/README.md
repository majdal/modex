pubsub.ws
=========

Pubsub should be handled entirely server side. A "topic" should be websocket URL.
"subscribing" should be connecting to that URL, and "publishing" should be .send()ing to it (which then is reflected back to all listeners)
