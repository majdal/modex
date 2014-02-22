
# Goal

# Issues

We need to solve

How do we handle updating map items? Do we push them over the websocket directly,
do we push a notification that the frontend should reget
or do we just have the frontend polling every tile every second?

And when we **do** get new data, how do we make sure we're updating
polygons and tiles instead of overlaying?
(without checking first) It seems like the default behaviour of mapping
libs is to cache heavily; the initial motivation of tiling is to cache
 and be efficient; 

people have got dynamic maps with d3 here and there...

# APIs for Comparison

## 

## D3

* Raster:
* Vector:

## OpenLayers

* Raster: http://ol3js.org/en/master/apidoc/ol.source.TileImage.html or one of its subclasses, like 
* Vector: http://ol3js.org/en/master/apidoc/ol.source.TileJSON.html ??

## Polymaps

* Raster: http://polymaps.org/docs/image.html
* Vector: http://polymaps.org/docs/geoJson.html
