TODO
====

We have a TODO list on a 'real' task tracker at Asana. These should be merged there eventually.


Orthogonal Tasks
-----------------

_"A Yak Shaved is a Yak Saved"_

These are things that would save us time and headache if we had them,
and that can be worked on indepedently of the critical path.

- [ ] PyGDAL: expand src/models/eutopia/pygdal.py into a full library
    - [ ] all SWIG classes wrapped nicely
    - [ ] unit tests
    - [ ] up on github and *maintained*
    - Lit review:
        - [ ] [PySal](http://pysal.readthedocs.org) -- is this relevant should it be rolled in? supported somehow?
- [ ] "jSQL": some sort of javascript frontend + server backend which allows efficient *and secure* querying (but not updating!) of databases.
    - [ ] Lit review: read up on how the pros deal with large datasets.
        - [ ] Miso's [Dataset](http://misoproject.com/dataset/) (tables; client side **only**, which is a weakness and a strength)
        - [ ] Square's [Cube](http://square.github.io/cube/) (events)
        - [ ] Square's [Crossfilter](http://square.github.io/crossfilter/) (tables; client side and, somehow, high performance)
        - [ ] [Whisper](http://graphite.readthedocs.org/en/latest/whisper.html)
        - [ ] LINQ (Microsoft: SQL and Objects)
        - [ ] Dublin Core
        - [ ] OWL (objects!)
        - [ ] grano (networks!)
        - [ ] n3/SparQL (objects!)
        - [ ] SQL (tables + relations)
        - [ ] Haskell and Python's list comprehensions (objects!)
        - [ ]  _____????____ (plain, denormalized, one table csv/tsv/xls) approach the task of information storage, organization, and retrieval.
        - [ ] Maps:
            - [ ] http://trac.mapfish.org/trac/mapfish/wiki/MapFishProtocol (GeoJSON) 
            - [ ] See OpenLayers.Protocol.* from [ol2](https://openlayers.org)
            - [ ] WMS/WFS
    - [ ] Implementation
- [ ] wrap modelling framework parameters sweeps into something that Model Runner can use and manipulate
    - [ ] input  (--> shell command line?)
    - [ ] output (--> csv?)
    - for each of:
        - [ ] RepastSimphony
        - [ ] NetLogo
        - [ ] R (this should be relatively easy..)
        - [ ] Python (see: GarlicSIM for inspiration but not dogma)
- [ ] browser visualization lib
    - Mostly this will be collecting things which already exist:
    - [ ] Network
    - [ ] Sankey Diagrams
    - [ ] also requires wrapping each of the above to conform to the DataBind API ([whatever that turns out to be, which we don't have clear yet]) 
- [ ] widgets
    - [ ] build the <slider> tag into a whole HTML5-based date slider
    - [ ] add a <input type="month"> (not date or week, those are too fine; there's no "year" control tho) to give clickable control over time -- [this is only supported in WebKit so far, but by the time we're done the others will have caught up]
- [ ] 
- [ ] Sensible data subsampling [this task will be very, very, very involved]
    - It doesn't seem to be too difficult for javascript (at least on a modernish laptop or better) to store a large amount of data
      (in fact, [Crossfilter can handle 5mb of tables or more](http://square.github.io/crossfilter/)),
       rendering it all is a very different story.
       For maps, mbostock wrote Dynamic Path Simplification, which is now rolled into topojson;
       for line graphs we can do a rolling average or something.
       For a relatively simple relationship (e.g. linear or cubic), a linear subsample (e.g. in python, `s[::1000]` selects every 1000th point) is appropriate--fast, too--but will miss important details applied blindly.
   - The task is: write a library, subroutine, widget, or _something_ which makes culling
     generic datasets to a viewable size reusable and simple.
   - What it means to interact with a piece of scaled UI is complicated!
     If you've averaged points on a line graph, does clicking zoom in to those points or display a popup listing those points?
     If you've path-simplified a map (and just to be fiddly, suppose the simplification happened to blur provincial boundaries),
       does clicking a block show data from both provinces?
       Getting this right means the simplification cannot throw away all of the relationships, but it is unclear what it should keep.
   - Lit review:
       - [ ] Microsoft's [SemanticZoom](http://msdn.microsoft.com/library/windows/apps/hh702601)
       - [ ] Audacity's [waveform display](https://svn.FIXME) switches rendering methods below a certain hardcoded threshold -- but this is strictly only appropriate for waveforms, like audio and maybe seasonal timeseries.
   