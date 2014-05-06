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
- [ ] "jSQL": some sort of javascript frontend + server backend which allows efficient *and secure* querying (but not updating!) of databases.
    - [ ] Lit review: read up on how
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