# PyGDAL

GDAL is a C++ library that has been SWIG'd into several other languages.

As it is, it is not very pythonic:
 errors are noted as "None" + asking for what the error was,
 loops must be written by index (there's no iterators, despite the datastructures that GDAL deals with largely being lists)
 properties are accessed by layer.gethtepropertysomethingiforgetthenameofthismethod("name") instead of layer["name"] or layer.name
 
We can do better.
