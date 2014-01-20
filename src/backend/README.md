# Backend Developer's Readme

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

## Gotchas




You must run the server under python2. Twisted is [the largest](https://wiki.python.org/moin/Python2orPython3) library yet to be ported to python3.

In twisted, node.putChild() must have its first argument **NOT** end with a '/'. That will cause mysterious 404s with no clue in the log.

In OL3, when loading Vector layers, you (for some currently unknown reason) must pass 'renderer: ol.RendererHint.CANVAS' to the Map constructor or else they will fail with a nil ptr exception in the bowels of OL.


## Compatibility

we should at least cover:
Installing the server on
* Ubuntu
* Mac
