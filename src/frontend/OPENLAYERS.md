# Guide to OpenLayers

1) Run a development webserver on your machine. This will make your life ages easier in working with OL.
2) OpenLayers comes in a stable v2 (openlayers.org) and an unstable "but probably better (TM)" v3 (ol3js.org)
  * We're thattempting to use v3, but there's still lots of undocumented parts that require good guesswork and knowledge of object orientated style.
  * This file is a kludge to fill in those gaps until OL3 gets stable


### Setting object properties
Properties are given json-style to class constructors:
each constructor takes a single dictionary (aka javascript object aka something written like
 "{ ... name: value, name: value, ... }").
This looks like
```javascript
new ol.layer.Tile({
                   opacity: .5,
                   source: new ol.source.OSM()
                  })
```

 By digging through the OL3 [source code](https://github.com/openlayers/ol3/tree/master/src/ol/layer)
 you can figure out the names of properties that objects will take. This can be sort of tricky though.
 For example, that "opacity" property is something that we knew _should_ be supported by a mapping library
 but it wasn't documented.
 We found [one occurence](https://github.com/openlayers/ol3/blob/315c42f0a7bad339c96f2f936d7513a498df1b12/src/ol/layer/layer.js#L20)
 of it in the comments but nothing obvious in the code, so we just held our nose and tried it and it worked.
