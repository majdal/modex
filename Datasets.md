(Nick organized a starting list based on a brainstorm we did together.)

## Data Types

### To Sort
Weather?? (Light, Wetness)
  --this is tricky.

### Maps - Raster
1.   (Human) Wealth density
1.   Ground water
1.   Surface water
1.   Heightmap
1.   Population density (human, rabbit, fox, deer, butterfly, forest, dandelion
1.   Albedo
1.   Climate?? Temperature? Wetness?? unsure
1.   Soil type (are there subproperties here? like separate layers for nitrogen, oxygen, water..?)
1.     Location and type/quality of forests
1.     Population location and density
1.     Location of watersheds/rivers

  
 ### Maps - Vector
1.    Agent locations
1.    Major food warehouses (e.g. Food Terminal in Toronto - I think most of Ontario's food goes there)
1.    Roads, Highways, Rail, Shipping Routes, Ports, Backroads
1.    Watersheds
1.    Rivers / groundwater / lakes
1.    Political Boundaries:
     (country, provincial, municipal, township, Greenbelt / Bioregion boundaries, Food Safety Inspection Zones)

### Network
1.  Seller networks (directed)
1.  Social networks (undirected)
1.  Resource flow Networks
-  Food: directed
-  Money: bidirected
-  Manufacturing ((there's an open problem here: what does it mean to track resources as they transform? how do we visualize that?))
 
### Tabular
1.     What food processing is done 

1.     Farm level crop production (broadly by category)

1.     Quantity of food for (Ontario/rest of Canada)

1.     Properties of species

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

### Visualization Types?
1. Salience PlotsImp
1. Sheelagh's Transmogrifications

## For Now This Could Look Like
1) Table of Agents
 ---farmers
 ---processing plants?
 ---buyers (cities)

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
