(Nick organized a starting list based on a brainstorm we did together.)

## Potential Datasets

### To Sort

1. **Soils:** Canada>Ontario>Provincial ont_omafra: soils from omafra - Ontario's ministry of food and agriculture 1.75 GB
1. **Soils:** Agriculture department also gives soils.. (soils dataset is 130 MB) 
canada_dept_agriculture>waterloo soils_cansis>
1. **Provincial Political Boundaries:** Canada>Ontario>Provincial ont_greenbelt plan_2005 20 MB
1. **Temperature:** Canada>Federal>??agriculture nlwis_gridded climate.. anu_splin model GeoTif from the weather model (get). 7.43 GB total: 1/2 mb is a day 1 day temporal resolution 10 km spatial resolution and each day is 1/2 mb - 
1. **Property Ownership:** cadastral

### Sources
1. **Ontario Geospatial Data Exchange** (Waterloo is a member. We can use for academic purposes.)
1. **Omafra**
1. **Ontario Open Data** https://www.ontario.ca/government/open-data-ontario
1. **Esri** Writes ArcGIS and provides some maps including ones that OpenLayers can access. 
1. **DMTI**
1. **Teranet** Ownership (cadastral) data.


## Data Types

One of our todos, issue #22, is 

### Maps - Raster
(**NB**: rasters can be coerced with some resolution loss to vectors, so this list is only tentative)

1. (Human) Wealth density
1. Ground water
1. Surface water
1. Heightmap
1. Population density (human, rabbit, fox, deer, butterfly, forest, dandelion
1. Albedo
1. Climate?? Temperature? Wetness?? unsure
1. Soil type (are there subproperties here? like separate layers for nitrogen, oxygen, water..?)
1. Location and type/quality of forests
1. Population location and density
1. Location of watersheds/rivers

  
### Maps - Vector
(**NB**: vectors can be coerced with some resolution loss to rasters, so this list is only tentative)

1. Agent locations
1. Major food warehouses (e.g. Food Terminal in Toronto - I think most of Ontario's food goes there)
1. Roads, Highways, Rail, Shipping Routes, Ports, Backroads
1. Watersheds
1. Rivers / groundwater / lakes
1. Underground water: aquifers
1. Political Boundaries:
  * country
  * provincial
  * regional
  * municipal
1. Greenbelt / Bioregion boundaries, Food Safety Inspection Zones)

### Network
1.  Seller networks (directed)
1.  Social networks (undirected)
1.  Resource flow Networks
  - Food: directed
  - Money: bidirected
  - Manufacturing ((there's an open problem here: what does it mean to track resources as they transform? how do we visualize that?))
 
### Tabular
1. What food processing is done 
1. Farm level crop production (broadly by category)
1. Quantity of food for (Ontario/rest of Canada)
1. Properties of species

### Tabular: [Resource/Product I/O Rates](https://en.wikipedia.org/wiki/Input-output_model)
* Farming methods
* Farm productiveness by land-type

### Time Series
1.  GDP / Overall / Average Wealth
1. Health metrics
1. Carbon
1. ??????
1. Standardized educational testing scores

### Casuality
1. How land/light/warmth etc modifies production of goods by farms
1. How roads/people/land/light/warmth etc modifies survival of species
1. Input/output table of production techniques

### To Sort
Weather?? (Light, Wetness)
  --this is tricky.


# Mockup
For getting the ball rolling, let us invent datasets and put them under assets/data/, in .csv, .dot, and .shp formats.

1) Table of Agents
 - farmers
 - processing plants?
 - buyers (cities)
2) Map (Vector layer--possibly just a sketch in photoshop) of Agents
3) Road Network
4) Raster: Wealth Distribution for each of 6 time steps
5) Raster: Water distibution for each of 6 time steps
Raster: land cover type? (or should this be split into soil type/water/...?)

6) Raster: Forest distribution for each of 6 time steps

Raster: Habitat for each of 3 species

Timeseries (for 6 time steps): GDP

Timeseries (for 6 time steps): Carbon

I would really like to include weather in here, but weather is neither raster, vector, nor time series. It's several interacting vector fields as functions of time--which we could think of as a raster, and that is what the radar maps show, but I am unsure of the best practice here
