
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
There's some provision for custom tile sizes; there's a "tileSize" arg you can put in as a param to a TileGrid..
but I don't see how to, and the [co](https://github.com/openlayers/ol3/blob/d9437e469d8bec9c908e7e336785fb2c1a36a54b/src/ol/tilegrid/xyztilegrid.js#L32)/[de](https://github.com/openlayers/ol3/blob/d9437e469d8bec9c908e7e336785fb2c1a36a54b/src/ol/source/bingmapssource.js#L86) makes it seem
like it's only really meant as an internal property.
More hints [here](https://groups.google.com/forum/#!searchin/ol3-dev/tile/ol3-dev/nIkURl6aXSE/TDp6ywwDQx4J) and [here](https://groups.google.com/forum/#!searchin/ol3-dev/tile/ol3-dev/oG1lQYTiVSA/gIlC7CtvqsoJ).



It seems that 
OpenStreetMap provides vector tiles; however they are generated from their backend DB, and asking for an empty area
or even an area that's not even valid just gives """{"type":"FeatureCollection","features":[]}""". So we need to
understand a priori what the right area codes to use are; simply ripping down tiles isn't going to help us.

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
