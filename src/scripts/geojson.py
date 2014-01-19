# geojson.py
# 
# ---copyright goes here---
# this is python2 code
# requirements: gdal with its python bindings installed

import os
import osgeo.ogr as ogr
ogr.UseExceptions() #make ogr closer to sane
assert ogr.GetUseExceptions() == True


#import geojson


#functions we care about:
# ogr.open() (not, not gdal.open, that's for rasters!!)
# layer.TestCapability("FastSpatialFilter")
# layer.GetFeatureCount()
# feature.geometry()
# layer.SetSpatialFilterRect()
# feature['key'] 

import IPython
IPython.terminal.embed.TerminalInteractiveShell.confirm_exit=False #i want
#IPython.get_config().InteractiveShell.confirm_exit = False

def features(shapefile):
	"a simple iterator that returns items from a shapefile"
	"precondition: your shapefile has exactly one layer (you can split it up with gdal or qgis if this is not true)"
	input = ogr.Open(shapefile)
	assert input.GetLayerCount() == 1, "This simple iterator only supports single-layer files"
	
	layer_in = input.GetLayerByIndex(0);
	return (layer_in.GetFeature(f) for f in range(layer_in.GetFeatureCount()))




def filterrect(polygons, left, right, bottom, top):
	"ogr::Layer::SetSpatialFilterRect seems to be buggy, or I'm misunderstand the docs"
	"this hack implements it plus the iteration to actually extract filtered features"
	"note that the order of arguments is flipped to my intuition (and what ogr::Geometry::GetEnvelope() returns...) says they should have"
	
	if isinstance(polygons, str):
		polygons = featues(polygons)  #I *believe* that this should (even if polygons happened to already be opened)
	
	def p_inrect(point):
		"return true if the point ... is"
		raise NotImplemented
	
	def inrect(geometry):
		"a 'geometry' is a point, line, or polygon, or compositions thereof"
		"i.e. something on the map"
		assert geometry.GetGeometryType() == ogr.wkbPolygon, "TODO: support more than just polygons"
		
		
	# extract the geometry object that gdal creates when we call it
	layer.SetSpatialFilterRect(left, bottom, right, top)  
	clip = layer.GetSpatialFilter() 
	layer.SetSpatialFilter(None)   #unset the filter since we're doing it manually
	def gen():
		for f in polygons:
			if f.intersects(clip):
				yield f
	#return layer.


#todo: write generic filtering thing

def filter_to_elora_really():
	driverName = "ESRI Shapefile"
	
	# near Elora, Ontario, which is
	# #  -80.42722 , 43.685
	# the lat/lon system is deformed so that
	# # a unit latitude is 8.3km, and a unit longitude is 10km (<-- is this right??)
	# for ourpuroses, taking a couple of degrees in each direction should be good ... 79 to 81 
	elora = ((-81, 42), (-79, 44)) #(bottomleft, topright), to be in line with SetSpatialFilterRect()

	shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"
	input = ogr.Open(shapefile)
	
	drv = ogr.GetDriverByName( driverName )  #construct driver object for output file
	if drv is None:
		raise RuntimeError("%s driver not available.\n" % driverName)
	
	output_shapefile = shapefile+"_filtered"
	
	if os.path.exists(output_shapefile):
		import shutil
		shutil.rmtree(output_shapefile)
	
	output = drv.CreateDataSource(output_shapefile)
	if output is None:
		raise ValueError("Creation of output file '%s' failed" % output)
	
	# the code below was mostly adapted from the python example at
	# http://www.gdal.org/ogr/ogr_apitut.html
	for layer_in in (input.GetLayerByIndex(l) for l in range(input.GetLayerCount())):
		print(layer_in.GetName())
		((left, bottom), (right, top)) = elora;
		layer_in.SetSpatialFilterRect(left, bottom, right, top)  
		clip = layer_in.GetSpatialFilter().Clone()
		
		layer_in.SetSpatialFilter(None)   #unset the filter since we're doing it manually
		
				
		# all good? make the destination Layer
		layer_out = output.CreateLayer(layer_in.GetName()+"__elora",
		                               layer_in.GetSpatialRef(),
		                               layer_in.GetGeomType())
		
		if not layer_out:
			raise RuntimeError("Layer creation failed.")
		
		# we need to clone the schema to the new layer
		# if we don't do this, the code will run and will copy records
		# but the only data will be the FIDs (which are generated upon adding)
		schema = layer_in.GetLayerDefn();
		for field in (schema.GetFieldDefn(i) for i in range(schema.GetFieldCount())):
			layer_out.CreateField(field)
		
		copied = 0
		for i, feature in enumerate((layer_in.GetFeature(f) for f in range(layer_in.GetFeatureCount()))):
			#print "Reading FID",feature.GetFID()
			#g = feature.geometry()
			#print(g)
			#print(clip)
			#IPython.embed()
			if not clip.Intersects(feature.geometry()):
			#	print "Skipping FID",feature.GetFID()
				continue
			if layer_out.CreateFeature(feature) != 0:
				raise RuntimeError("Failed copying feature FID%d to shapefile '%s'." % (feature.GetFID(), shapefile_out))
			copied += 1
			if i % 10000 == 72:
				print "Copied", i, "records"
			
		print "Copied", copied, "records"
		
		assert output.SyncToDisk() == 0, "Failed to save!" #XXX better error needed
	


def filter_to_elora():
	"attempt to programmatically filter the ARI dataset to only those elements that are relevant to our interests"
	"this is buggy: gdal doesn't behave like the docs say it should"
	driverName = "ESRI Shapefile"
	
	# near Elora, Ontario, which is
	# #  -80.42722 , 43.685
	# the lat/lon system is deformed so that
	# # a unit latitude is 8.3km, and a unit longitude is 10km (<-- is this right??)
	# for ourpuroses, taking a couple of degrees in each direction should be good ... 79 to 81 
	#elora = ((-81, 42), (-79, 44)) #(bottomleft, topright), to be in line with SetSpatialFilterRect()
	
	
	#this dataset is courtesy http://geo2.scholarsportal.info/
	# originally from http://lioapp.lrc.gov.on.ca/edwin/EDWINCGI.exe?IHID=6&AgencyID=35&Theme=AGRICULTURE
	# which is now quite dead
	# we do not have a license to distribute it, so you will need to go to that site,
	# find "Agriculture Resource Inventory", download and unzip it.

	shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"
	input = ogr.Open(shapefile)
	
	drv = ogr.GetDriverByName( driverName )  #construct driver object for output file
	if drv is None:
		raise RuntimeError("%s driver not available.\n" % driverName)
	
	output_shapefile = shapefile+"_filtered"
	
	if os.path.exists(output_shapefile):
		import shutil
		shutil.rmtree(output_shapefile)
	
	output = drv.CreateDataSource(output_shapefile)
	if output is None:
		raise ValueError("Creation of output file '%s' failed" % output)
	
	
	# the code below was mostly adapted from the python example at
	# http://www.gdal.org/ogr/ogr_apitut.html
	for layer_in in (input.GetLayerByIndex(l) for l in range(input.GetLayerCount())):
		print(layer_in.GetName())
		assert layer_in.TestCapability("FastSpatialFilter"), "Layer '%s' does not support fast spatial filtering; bailing" % layer_in.GetName()
		
		# all good? make the destination Layer
		layer_out = output.CreateLayer(layer_in.GetName()+"__elora",
		                               layer_in.GetSpatialRef(),
		                               layer_in.GetGeomType())
		
		if layer_out is None:
			raise RuntimeError("Layer creation failed.")
		
		feature_schema = layer_in.GetLayerDefn() #this produces an instance of FeatureDefn, which essentially just defines several fields and is an awful lot like a class. It's like this since this is C++ wrapped by SWIG and C++ doesn't have class-objects so GDAL has no way to represent such a meta concept
		
		#layer_in.SetSpatialFilterRect(-79, 42, -81, 43) #this one gives a strange result... it seems to mark out a rectangle of some sort, yet..not really??
		#layer_in.SetSpatialFilterRect(minx, miny, maxx, maxy)
		#layer_in.SetSpatialFilterRect(-83, 43, -82, 44)  #this seems to be filtering *out* everything in this layer
		layer_in.SetSpatialFilterRect(-82, 44, -83, 43)  #flipped??
		
		#attempt to debug SetSpatialFilterRect() by printing its output to the map
		filter_rectangle = layer_in.GetSpatialFilter();
		#assert layer_out.CreateFeature(filter_rectangle) == 0;
		print "filter", filter_rectangle.ExportToJson()
		
		filter_feature = ogr.Feature(feature_schema)
		filter_feature.SetGeometry(filter_rectangle)
		assert layer_out.CreateFeature(filter_feature) == 0
		
		# we need to clone the schema to the new layer
		# if we don't do this, the code will run and will copy records
		# but the only data will be the FIDs (which are generated upon adding)
		schema = layer_in.GetLayerDefn();
		for field in (schema.GetFieldDefn(i) for i in range(schema.GetFieldCount())):
			layer_out.CreateField(field)
		
		#.SetWidth(32)?????
		#print(filter_feature.keys())
		#raw_input("About to copy all the %d datums" % layer_in.GetFeatureCount())
		for datum in (layer_in.GetFeature(f) for f in range(layer_in.GetFeatureCount())):
			#print(datum.keys())
			#IPython.embed()
			if layer_out.CreateFeature(datum) != 0:
				#XXX this crash should list the layer name its copying too as well
				raise RuntimeError("Failed copying feature FID%d to shapefile '%s'." % (datum.GetFID(), shapefile_out))
			
			#datum.Destroy() #save memory?? (this doesn't seem to affect memory use at all..)
		layer_in.SetSpatialFilter(None) #undoe the filtering
		#doing the sync after the loop speeds this up by a factor of 18
		assert output.SyncToDisk() == 0, "Failed to save!" #XXX better error needed
	
	

def geojson(shapefile):
	"dump a shapefile to GeoJSON"
	
	dataset = ogr.Open(shapefile)
	#print ("Loaded it, yo")
	
	for l in range(dataset.GetLayerCount()):
		layer = dataset.GetLayerByIndex(l);
		#print layer.GetName(), "has these coordinates", layer.GetExtent()
		#print "which are relative to this reference:"
		#print str(layer.GetSpatialRef())
		#print "%s has %d elements" % (layer.GetName(), layer.GetFeatureCount())
		#return;
		
		for f in range(1, layer.GetFeatureCount()):
			feature = layer.GetFeature(f)
			print feature.ExportToJson()
			#IPython.embed(); break;
			#print datum.keys()
			#MAP_DESCR
			#_p = "%s, %s{FLEXSPACE}(%.3f, %.3f)" % (datum['name'], datum['city'], datum.geometry().GetX(), datum.geometry().GetY())
			#_p = "FID%d:{FLEXSPACE}(%.3f, %.3f)" % (datum.GetFID(), datum.geometry().GetX(), datum.geometry().GetY())
			#_p = _p.replace("{FLEXSPACE}", " "*(80 - (len(_p) - len("{FLEXSPACE}"))))
			#print _p


if __name__ == '__main__':
	import sys
	shapefile = sys.argv[1]
	geojson(shapefile)
	#main()
	#filter_to_elora_really()
