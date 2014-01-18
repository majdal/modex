**Backend**

![Architecture Diagram](Architecture.png)

# Major Components
## Backend

 Probably Python/Scipy
 GDAL (for geographic data)
 [http://repast.sourceforge.net/](Repast)?
 

   current plan is to build an app in python using [Twisted](http://twistedmatrix.com/trac/) which hosts [[GarlicSIM]] models, and handles recording data
### Model
* [[GarlicSIM]]
* [[Modelling]]

### Model Explorer
  A major component for us is a tool at some remove from the nitty details of the rest of the system for exploring models in general. This wiki is in the "modex" repository right now, reflecting the importance of this tool. It might also be called the Simulation Host, which in an [IoC](http://en.wikipedia.org/wiki/Inversion_of_control) way, loads and collects results from simulation runs. It should be able to easily record, slice and visualize any aspect of the simulation. The closest work we have in mind is tcstewar's [ccmsuite](https://github.com/tcstewar/ccmsuite) and (the unmaintained) [GarlicSim](https://github.com/cool-RR/GarlicSim) (in fact we might just take up maintenance GarlicSim). Also, for the sake of getting other research groups interesting, using, and eating our own dogfood, the simulation host should be as platform agnostic as possible.

Model Explorer's duties are:
 * load models
 * batch run lots of copies of a model
   * clearly distinguish and provide hooks for handling deterministic models sampled at different initial conditions, nondeterministic models sampled several times at the same initial conditions, and mixtures
 * provide a consistent data API (similar to how Repast collects several timestepping and geographic APIs in one place)
 * provide a consistent data logging API
 * generate plots
 * generate statistics (estimates, probability densities, condidence intervals) -- and plots of these where relevant (eg estimated temperature on a map, estimated sensitivity field across a state space plot)
 * 

**Aspects** is a key word here, as even a simple five-object model has 5 objects each of which could have some arbitrary number of variables of interest (weight, tempurature, wealth, happiness, ...) and 5-choose-2=10 pairs which means that any relationship of interest has 10 series that need tracking, and all of this is potentially recorded over time. We need to have a tight way to record this information, and a tighter way to reduce it to useful slices.
   ([ccmsuite](http://github.com/tcstewar/ccmsuite), or whatever develops to replace it)

### Importing (csv, shapefile, graphviz)
  [[Datasets]]

### Exporting (csv, graphs)


## Frontend

  The frontend should appear to be an attractive video game, but one where graphs and data can be brought up at a moments' notice. We're ambitiously attempting to gamify science.

 HTML5 (websockets, json, probably d3.js, maybe craftyjs, openlayers: http://ol3js.org/ (v3-beta) / openlayers.org (v2))

 craftyjs: for rendering agents, at a low enough zoom level
 d3: for making charts and plots
 openlayers: for rendering **and** interacting with maps, where we consider a map both the baselayer, and overlays like raster density plots, and vector features.
  * we can feed it raster data with its built in support for tiles, including common sources like MapQuest, Google, and Bing, and feed it vector data with .gml, .kml, or geojson. 



### Rendering (see [[Visualizations]])
  * 
  * we're thinking of using d3.js and/or craftyjs.org
  ---interactives
## UI (partially crossed with Rendering)
   ?????  



## Unstructured Comments That Should Be Reorganized Please

### Parallelization
 A single run of the model will probably be highly CPU bound and serialized, but we have a chances for parallelization at these points:
 * rendering
 * running multiple model runs, to get better statistics
 * getting bootstrap statistics

 