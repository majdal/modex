Here we list all the APIs and platforms we have considered. It is a serious time sink to research the suitability of a platform, so with the reasons we have kept or rejected, or put  each on hold.


## Frontend

HTML5 is extremely powerful. It has a lot of new widgets (under form elements: sliders, numbers, dates, file uploaders, also <progress> and <meter> which lists). We can probably build most of our widgets direct in HTML.

* craftyjs?
* [TogetherJS](https://togetherjs.com/) by Mozilla for adding commenting throughout a site
* [Modernizr](http://modernizr.com/) to let us write one codebase against HTML5

### Maps

* OpenLayers: [2](http://openlayers.org) and [3](http://ol3js.org)
  * we should see if we can divert some part of our budget to them: http://www.indiegogo.com/ol3
* http://tilestache.org/
* http://polymaps.org/
* [ModestMaps](http://modestmaps.com/examples/)
(_these all seem like they overlap a bit; what's the deal?_)

### Data
* d3js
* [cubism.js](http://square.github.io/cubism/) for visualizing live time series data
* [cube](http://square.github.io/cube/)
* [graphite](http://graphite.wikidot.com/)
* [dimplejs](http://dimplejs.org/)

* HTML5

## Networking

* [WebSockets](http://www.websocket.org/quantum.html)
* [EventSource](http://stackoverflow.com/questions/8499142/html5-server-side-event-eventsource-vs-wrapped-websocket)
* jsonp

* Autobahn
  * Tutorials do not work at this time. Re-evaluating our use of Autobahn.
* [SockJS-twisted](https://github.com/DesertBus/sockjs-twisted/); see also [SockJS-client](https://github.com/sockjs/sockjs-client) for drop-in websocket support for older browsers

* [ws4py](https://github.com/Lawouach/WebSocket-for-Python)
* [cherrypy](http://www.cherrypy.org/)
* [txWS](https://github.com/MostAwesomeDude/txWS)



## Backend
* Twisted
* Django
* [RPy](http://rpy.sourceforge.net/rpy2.html) and its child [rmagic](http://ipython.org/ipython-doc/dev/config/extensions/rmagic.html) to hook out
* Jython to wrap java code??
* [PIL](http://pillow.readthedocs.org/) for generating and working with rasters

Webby stuff:

* Jinja2==2.7.1
* MarkupSafe==0.18
* Werkzeug==0.9.4
* klein==0.2.1



* PostGIS

### Video??

* ??? ?? ? ? ?

## Patterns
* REST
* Pub/Sub
* Events
* Declarative (e.g. d3)

## Modelling
* Repast
* GarlicSIM
* [PyABM](http://www-rohan.sdsu.edu/~zvoleff/research/pyabm/) (canonical usage example [here](https://github.com/azvoleff/chitwanabm/blob/master/chitwanabm/agents.py))
  * check out [what wikipedia thinks](http://en.wikipedia.org/wiki/Comparison_of_agent-based_modeling_software) to be bored to tears
* [ABCE](https://github.com/DavoudTaghawiNejad/abce) _Agent Based Complete Economy_ (python); [paper](http://jasss.soc.surrey.ac.uk/16/3/1.html)
* http://insightmaker.com/

## Tools

* [GeoHack](https://tools.wmflabs.org/geohack/) (all lat/lon coordinates on Wikipedia link to GeoHack)
* [MapBox Collaboratory](https://www.mapbox.com/)

## Collaboratories

* [StackExchange](http://stackoverflow.com/) - _they've thought long and hard -- and have measured -- about the right way to do comment systems; the link escapes me right now, though -kousu_

* [DIY.org](http://diy.org/)
* [jsFiddle](http://jsfiddle.net) -- [example](http://jsfiddle.net/sharavsambuu/s7QjN/9/light/)
* [Tributary.IO](https://github.com/enjalot/tributary.io): Rapid Collaborative D3 Prototyping

* asana.com -- project management
* github
* academia.edu??
* 

* [nbviewer](http://nbviewer.ipython.org/) which lets scientific people show off their [ipython notebooks](http://ipython.org/notebook.html), like [this one](http://nbviewer.ipython.org/urls/raw2.github.com/damontallen/Orbitals/master/Hydrogen%20Orbitals%20-%20working.ipynb)

### Dataset Management
* http://dat-data.com 
* http://datahub.io
* (there's at least two other dataset-version-control/archival sites; what are they?)
* https://exversion.com

### Citation Management
* http://www.zotero.org/
* http://www.mendeley.com/


## Blogs
* wordpress
* mezzanine (on django)
