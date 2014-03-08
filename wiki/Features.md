Features
========

This is our official Model Explorer feature spec. It is expected to evolve with time. 
See [UseCases](UseCases.md) for the motivation behind all of these
(or, if you can't find it there, challenge the feature in a comment here or write up a case study there)


## V0.01

1. A running farm model
  * State:
    1. Farms (polygons)
    2. Farmers (agents)
    3. Distributors (agents)
    4. Tax policy (parameter)
  * Output:
    1. Some estimate of GDP
    2. Carbon?
1. Able to trivially open up a web browser and see the farm model -- basically NetLogo but better
  * so we need data-binds or at leastt o fake them
2. Aesthetically pleasing
3. A single user

## V1

What would it take for us to feel that modex was "feature complete"?

1. Still single-user
1. Running a single instance of a model and "watching" it (see NetLogo for great examples of this)
1.  Interacting with a model it as it runs
  * Terry and Nick think that the only way to deal with this is for each model to define an API (eg "move forward", "implement this tax intervention", "drag), and Nick thinks that _modex_ should be agnostic about sending the interventions: if you want to record that an intervention happened you must go onto the server and edit the model to do record it as a piece of data, which then becomes plottable in the usual modex way
1. Able to host **any** (computational) model in **any** programming language, except that the model might need to be modified to output data in a particular way
1. Running many copies of a model in parallel and saving the results all to a single database
  * this feature includes the feature of parameter sweeps, which are super useful and superhard
1. Automated statistics generation
  * variances
  * means
  * medians
  * kernel density estimates
1. A way to write an expression which slices a subset of data from the backend
1. Handy, composable, data widgets, which are data-bindable (ie automagically update as new data comes):
  * the ability for end-users to compose new visualizations in-browser
  * these widgets need to be pretty
  1. Spreadsheets (ie tables)
  2. Network visualization
    * dynamic
    * hairball(ew) aka force-directed
    * tree-ish
    * ???
  1. Maps
    * vector data
    * raster data
    * objects on the map should be clickable and sensible related information from the other data streams should pop up
  1. Bar charts
    1. Bar charts with confidence and/or credible intervals
  1. Line graphs
    1. Line graphs with confidence and/or credible intervals
  1. Histograms
  1. Scatterplots
  1. 
1. Data-binds
2. Data-flows
2. Handy, composable, control widgets
  1. Sliders
  2. Number Dials
  3. Map widgets(????)
1. Data export
1. A small but effective suite of **forkable** example visualizations
1. A useful set of unit tests

## V1.5
1. Solid Suite of unit tests
 
## V2
1. (_World Wide_) Web-based Collaboration 
  1. Permalinks for each visualization and model run
  2. Multiuser (so sessions)
  1. (optional) user identities (Facebook connect, Mozilla Persona, OpenID, plus a site-custom account db)
  2. Comments, comments, everywhere
  2. Forking of explorations

## V2.5
1. More unit tests

## V3

1. Forking of models
  * if we are supporting _any_ model in _any_ language, then in general this is impossible: to fork a model you must fork that codebase. But we can ease the pain if we make setting up the server on your own machine easier and help model writers make their models easier to fork (by reducing or including dependencies)
1. (painlessly) Locally runnable:
  1. Windows installer
  2. Mac installer
  3. Clean builds for linux, and attempts to get it into package managers (especially arch and debian)
2. Datasource mashups (so, Stanford should be able to host a repo of websocket-accessible (well, maybe RESTful, and then we wrap that in websockets) data sources 
3. Examples of mashups taking modex-server sources + links at data.gc.ca to do model validation (or to do model invalidation!)

## V3.5
1. More unit tests
