#!/usr/bin/env bash
# server-side for chat.html
# the server is totally barebones; all it is is a router,
# with zero security or flood controls

# implemented using fancy cleverness hidden in pubsub's __main__
python2 pubsub.py 8080 /chatrooms/ireland
