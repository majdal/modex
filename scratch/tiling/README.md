
# Goal

# Guide

To try out the raster tiling demos,
make sure you have the python imaging library installed (currently it must be the PILlow fork) and
run 'gen.py leser/' and wait for a bunch of pure-colour demo tiles to be made. These tiles are not committed to the repo because they're half a gig in all.
You might need to run a local web server (see our frontend developer's guide) in this directory depending on the combination of browser and example.

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

Hm. It seems that OpenLayers demands tiles to be 256x256; if not, Chrome renders as so:
![borkychrome](tiles64x64-borkychrome.png)
and firefox simply doesn't render anything:
![emptyfox](tiles64x64-emptyfox.png)


# APIs for Comparison

## 

## D3

* Raster:
* Vector:

## OpenLayers

* Raster: http://ol3js.org/en/master/apidoc/ol.source.TileImage.html or one of its subclasses, like 
* Vector: ??

## Polymaps

* Raster: http://polymaps.org/docs/image.html
* Vector: http://polymaps.org/docs/geoJson.html
