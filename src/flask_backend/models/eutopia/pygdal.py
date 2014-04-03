# pygdal.py
"""
GDAL Wrappers to make dealing with GDAL less ridiculous.
Very work-in-progress.

There is another PyGDAL in PyPi, but it's unfinished.
"""


"""
words to the wise:
 the data model here has all children holding a parent pointer
 in raw GDAL this will crash:
  ```
   self.map = ogr.Open(SHAPEFILE).GetLayer(0);
   self.map.GetGeomType()
  ```
  because the shapefile (the value of "ogr.Open()") finds itself reference-count-less after the first line
  and self-destructs
   but then Layer::GetGeomType() must be trying to call up into that object
    and causes a pure virtual function call
  The python GC causing terrible inconsistencies in the C++ layer is a nether I want to bottle and keep far away.
"""

import os, zipfile, tempfile, shutil

import json #GDAL has ExportToJSON so so should PyGDAL


__all__ = ["Shapefile", "Layer", "Feature"]

#import gdal
import ogr
ogr.UseExceptions()

# stash the OGR magic constants, mostly to make debugging easier
ogr.CONSTANTS = dict((e, ogr.__dict__[e]) for e in ogr.__dict__.keys() if e.startswith("wkb"))
# but while we're at it, export them (until we have a full wrapper and can hide them behind types and/or enums)
globals().update(ogr.CONSTANTS)
__all__.extend(ogr.CONSTANTS.keys())

def invertOGRConstant(value):
    "given a value, find the names of the constants that goes with it"
    "i'm sorry; this is really just a quick hack for debugging and should be replaced by wrapping the OGR constants in enum objects"
    return [n for n in ogr.CONSTANTS if ogr.CONSTANTS[n] == value]

class Shapefile(object):
    "XXX this needs unit tests, badly"
    "wraps an ogr.DataSource to be less ridiculous"
    "Idea: give all members a pointer to this class, so that (but maybe this would be a terrible memory-hogging mistake..)"
    "then, so long as at least one feature from this shapefile is pointed to from the main program, the whole datastructure will stick around"
    def __init__(self, fname):
        if zipfile.is_zipfile(fname):
            #the logic here should be:
            # check if zipfile, if so unzip and continue as if that didn't happen
            #TODO: support writebacks to a zipped Shapefile (VERY COMPLICATED)

            self._unzipped = tempfile.mkdtemp()
            with zipfile.ZipFile(open(fname, "rb")) as zhp: #open the zipped shapefile
                zhp.extractall(path=self._unzipped)

            fname = self._unzipped

        self._source = ogr.Open(fname)
        if self._source is None: #an error occurred, but (by experiment) OGR won't tell us what it is
            #this should be FileNotFoundError, but we're stuck in Python2
            raise IOError("Unable to read shapefile '%s'" % (fname,))

    def __del__(self):
        "on finalization, clean up after ourselves"
        if hasattr(self, '_unzipped'):
            del self._source  #we need to close the source before rm -r will work
            shutil.rmtree(self._unzipped)

    @property
    def name(self):
        return self._source.GetName()

    #make a Shapefile look like a list of layers (which, really, it is)
    def __len__(self):
        return self._source.GetLayerCount()

    def __getitem__(self, i):
        "shapefiles are indexable by layer indexes (ints) and by layer names (strings)"
        if isinstance(i, int):
            if not (0 <= i < len(self)):
                raise IndexError("%s only has layers %d through %d" % (self.name(),0, i))
                #TODO: return a Layer object (of appropriate subclass, even: PolygonLayer, LineLayer, PointLayer)
            l = self._source.GetLayerByIndex(i)
        elif isinstance(i, basestring): #py2 :(
            l = self._source.GetLayerByName(i)
            if l is None:
                raise IndexError("%s has no layer '%s'" % (self.name, i))
        
        assert l is not None, "We should have handled possible all code-paths where l could fail"
        l = Layer(l)
        l.parent = self #ditto @ comment in Layer.__getitem__
        return l
        

class Layer(object):
    "TODO:"
    "support queries (ie SQL) on the layer"
    "...it is probably worth writing this (and not just relying on list comprehensions) precisely because DBs are good at queries"
    def __init__(self, ogr_layer):
        if isinstance(ogr_layer, Layer): #support copy-construction
            ogr_layer = ogr_layer._source
        
        #otherwise, wrap a raw GDAL object:
        assert isinstance(ogr_layer, ogr.Layer)
        self._source = ogr_layer

    def __getattr__(self, a):
        "until this library is fleshed out, just proxy most Layer calls through"
        try:
            return self.__dict__[a]
        except KeyError:
            return getattr(self._source, a)

    @property
    def name(self):
        return self._source.GetName()

    def __len__(self):
        return self._source.GetFeatureCount()

    def __getitem__(self, i):
        if not (0 <= i < len(self)):
            raise IndexError("%s only has layers %d through %d" % (self.name(),0, i))
        F = Feature(self._source.GetFeature(i))
        F.parent = self #parent pointers are set here instead of as a constructor arg because we don't necessarily know that Features are crafted out of a parent; but here in __getitem__ we do know that
        return F

    def __iter__(self): #XXX this particular piece of code seems so simple that it must be factorable
        for i in range(len(self)):
            yield self[i]

    def dumps(self):
        "GDAL doesn't have a layer.ExportToJSON()"
        "So we need to write it"
        "this line derived from the spec at http://geojson.org/geojson-spec.html#feature-collection-objects"
        return json.dumps({"type": "FeatureCollection", "features": [json.loads(f.ExportToJson()) for f in self]})


class Feature(object):
    "a simple wrapper that makes OGR Features objects pythonic"
    "every row in the table is exposed as a property"
    "this class is the start of scratch/pygdal"
    def __init__(self, ogr_feature):
        if isinstance(ogr_feature, Feature): #support copy-construction
            ogr_feature = ogr_feature._source
        
        #otherwise, wrap a raw GDAL object:
        assert isinstance(ogr_feature, ogr.Feature), "%s is not a ogr.Feature" % (ogr_feature,)
        self.__dict__['_source'] = ogr_feature #speak to __dict__ directly here because of dirty __getattr__ magic
    
    @property
    def geometry(self):
        return self._source.GetGeometryRef()

    def __getitem__(self, name):
        return self.__getattr__(name)
    
    def __setitem__(self, name, value):
        return self.__setattr__(name, value)
    
    def __getattr__(self, name):
        # check: local dict, then the fields (we can't access self.fields without accessing the local dict) and only then call up
        # TODO: provide access to .geometry()'s members directly (since, logically, a geofeature is the join of geometry and fields, not the parent fields with child geometry)
        try:
            return self.__dict__[name]
        except KeyError:
            try:
                return self._source.GetField(name)
            except:
                raise KeyError(name)
                #return getattr(self, name) #this causes an infinite loop

            #TODO: use
            #return object.__getattribute__(self, name) #very python2...  <http://stackoverflow.com/questions/3278077/difference-between-getattr-vs-getattribute-in-python>

    def __setattr__(self, name, value):
        # uh.. what's the rule here again?
        try:
            return self._source.SetField(name, value) #this causes infinite regress because it calls self.fields which triggers getattr
        except RuntimeError: #ogr gives this for all errors when UseExceptions() is on
            return object.__setattr__(self, name, value)
