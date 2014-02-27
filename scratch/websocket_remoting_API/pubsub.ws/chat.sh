#!/usr/bin/env bash
# server-side for chat.html
# the server is totally barebones; all it is is a router,
# with zero security or flood controls

# give helpful comments; run in the background (&) so that the comments show up after
# the server comes up but the server still has stdin and so can be killed by ctrl-c.
(sleep 2; echo; echo Now open http://localhost:8080/chat.html in your browser;
 sleep 2;       echo Then find a friend, give them your IP address, and point them to the same page.;
          echo) &

# launch pubsub broker using fancy cleverness hidden in pubsub's __main__
python2 pubsub.py 8080 /chatrooms/ireland

