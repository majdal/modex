# Model Explorer Developer's Guide

To get started, open a command prompt and run 'run.py' (which is living a directory up from here, in the project root):
```
[user@laptop modex]$ ./run.py
2014-01-19 22:57:35-0500 [-] Log opened.
2014-01-19 22:57:35-0500 [-] Starting server in /home/kousu/School/WICI/sig/repos/modex
2014-01-19 22:57:35-0500 [-] putting /home/kousu/School/WICI/sig/repos/modex/src/frontend at root
2014-01-19 22:57:35-0500 [-] putting /home/kousu/School/WICI/sig/repos/modex/assets at assets
2014-01-19 22:57:35-0500 [-] Site starting on 8080
2014-01-19 22:57:35-0500 [-] Starting factory <twisted.web.server.Site instance at 0x14cf680>
2014-01-19 22:57:35-0500 [-] Now open http://127.0.0.1:8080 in your browser
```

which should open a browser window pointed at the twisted web application server we're using.
Because of the complicated web-based nature of this project you must always be running the server
while developing, and you need to have a network connection available for at least for the basemaps, and perhaps other sources.

Next, depending on your purposes, see [frontend](frontend) or [backend](backend).
Some changes, namely API changes, which are going to be especially common in the early stage,
require working on both sides simultaneously. To do that work, keep both subfolders open and liberally restart the server: press Ctrl-C, wait for it to terminate, and then rerun 'run.py'.
