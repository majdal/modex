**Backend**
(todo: make a visio||svg diagram of the architecture, paste it in here)


**frontend:**
 HTML5 (websockets, json, probably d3.js, maybe craftyjs)

Backend:
 Probably Python/Scipy
 GDAL (for geographic data)
 [http://repast.sourceforge.net/](Repast)?

# Major Components
 Model
 Model Explorer ([ccmsuite](http://github.com/tcstewar/ccmsuite), or whatever develops to replace it)
 Importing (csv, shapefile, graphviz)
 Exporting (csv, graphs)
 Rendering (see [[Visualization]])
  * 
  * 
  ---interactives

 A single run of the model will probably be highly CPU bound and serialized, but we have a chances for parallelization at these points:
 * rendering
 * running multiple model runs, to get better statistics
 * getting bootstrap statistics


 
See more details at
* [[Modelling]]
* [[Datasets]]
* [[Visualizations]]