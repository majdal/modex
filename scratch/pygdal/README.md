# PyGDAL

GDAL is a C++ library that has been SWIG'd into several other languages.

As it is, it is not very pythonic:
 
 Exceptions are off by default (instead, errors are noted as "None" + asking for what the error was) and when they are on they aren't as nice as they could be
 loops must be written by index (there's no iterators, despite the datastructures that GDAL deals with largely being lists)

 as far as I can tell, it ~doesn't~ support zipped shapefiles which is just unnecessary
 GDAL freely frees stuff causing bad frees() and pure virtual functions calls;
    eg. self.map = ogr.Open(SHAPEFILE).GetLayer(0); self.map.GetGeomType() will CRASH with "pure virtual method called" 
     because the object that "ogr.Open()" is gets freed, but the Layer() one doesn't.

  the enums/magic constants in OGR/GDAL are exposed but not grouped in the python layer, making it difficult to know what they mean or deal with them elegantly
  
  adding columns is difficult; you need to access Schema object, find/copy a FieldDefn object, add it to the Schema, then update the Schema in the open Layer
   sure it might be dangerous (but that's what Read-Only is for) but if we could make this more active recordey or pythonic (like self.property = z) that would be cool man

at least it is possible to access properties by feature.propertyname (and also feature.GetField("propertyname"))

We can do better.
