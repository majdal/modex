**Backend**
(todo: make a visio||svg diagram of the architecture, paste it in here)


**frontend:**
 HTML5 (websockets, json, probably d3.js, maybe craftyjs)

Backend:
 Probably Python/Scipy
 GDAL (for geographic data)
 [http://repast.sourceforge.net/](Repast)?

# Major Components
 ## Backend
   current plan is to build an app in python using [Twisted](http://twistedmatrix.com/trac/) which hosts [[GarlicSIM]] models, and handles recording data
 ### Model
   [[GarlicSIM]]
* [[Modelling]]
 ### Model Explorer
  Some major component of this is a tool at some remove from the nitty details of the rest of the system for exploring models in general. It should be able to easily record, slice and visualize aspects. **Aspects** is a key word here, as even a simple five-object model has 5 objects each of which could have some arbitrary number of variables of interest (weight, tempurature, wealth, happiness, ...) and 5-choose-2=10 pairs which means that any relationship of interest has 10 series that need tracking, and all of this is potentially recorded over time. We need to have a tight way to record this information, and a tighter way to reduce it to useful slices.
  
   ([ccmsuite](http://github.com/tcstewar/ccmsuite), or whatever develops to replace it)
 ### Importing (csv, shapefile, graphviz)
  * [[Datasets]]
 ### Exporting (csv, graphs)


 ## Frontend
  the frontend should appear to be an attractive video game, but one where graphs and data can be brought up at a moments' notice.

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

 