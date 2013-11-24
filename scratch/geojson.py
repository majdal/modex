# geojson.py
# 
# ---copyright goes here---
# this is python2 code

import os
import osgeo.ogr as ogr
#import geojson

shapefile = "../assets/maps/_ags_DMTI_2010_CanMapRL_POI_AER_ALL_PROV2"

#
#this dataset is courtesy http://geo2.scholarsportal.info/#Metadata_Information
# originally from http://lioapp.lrc.gov.on.ca/edwin/EDWINCGI.exe?IHID=6&AgencyID=35&Theme=AGRICULTURE
# which is now quite dead
#shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"

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

def filter_to_elora():
	driverName = "ESRI Shapefile"
	
	# near Elora, Ontario, which is
	# #  -80.42722 , 43.685
	# the lat/lon system is deformed so that
	# # a unit latitude is 8.3km, and a unit longitude is 10km (<-- is this right??)
	# for ourpuroses, taking a couple of degrees in each direction should be good ... 79 to 81 
	elora = ((-81, 42), (-79, 44)) #(bottomleft, topright), to be in line with SetSpatialFilterRect()
	
	shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"
	input = ogr.Open(shapefile)
	
	drv = ogr.GetDriverByName( driverName )
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
		
		
		#layer_in.SetSpatialFilterRect(-79, 42, -81, 43) #this one gives a strange result
		layer_in.SetSpatialFilterRect(-79, 42, -81, 43)
		
		# we need to clone the schema to the new layer
		# if we don't do this, the code will run and will copy records
		# but the only data will be the FIDs (which are generated upon adding)
		schema = layer_in.GetLayerDefn();
		for field in (schema.GetFieldDefn(i) for i in range(schema.GetFieldCount())):
			layer_out.CreateField(field)
		
		#.SetWidth(32)?????
		
		#raw_input("About to copy all the %d datums" % layer_in.GetFeatureCount())
		for datum in (layer_in.GetFeature(f) for f in range(layer_in.GetFeatureCount())):
			if layer_out.CreateFeature(datum) != 0:
				#XXX this crash should list the layer name its copying too as well
				raise RuntimeError("Failed copying feature FID%d to shapefile '%s'." % (datum.GetFID(), shapefile_out))
			
			#datum.Destroy() #save memory?? (this doesn't seem to affect memory use at all..)
		layer_in.SetSpatialFilter(None) #undoe the filtering
		#doing the sync after the loop speeds this up by a factor of 18
		assert output.SyncToDisk() == 0, "Failed to save!" #XXX better error needed
	
	

def main():
	"for debugging"
	shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"
	
	dataset = ogr.Open(shapefile)
	print ("Loaded it, yo")
	raw_input();
	for l in range(dataset.GetLayerCount()):
		layer = dataset.GetLayerByIndex(l);
		print layer.GetName(), "has these coordinates", layer.GetExtent()
		print "which are relative to this reference:"
		print str(layer.GetSpatialRef())
		print "%s has %d elements" % (layer.GetName(), layer.GetFeatureCount())
		return;
		for f in range(layer.GetFeatureCount()):
			datum = layer.GetFeature(f)
			#IPython.embed(); break;
			#print datum.keys()
			#MAP_DESCR
			_p = "%s, %s{FLEXSPACE}(%.3f, %.3f)" % (datum['name'], datum['city'], datum.geometry().GetX(), datum.geometry().GetY())
			#_p = "FID%d:{FLEXSPACE}(%.3f, %.3f)" % (datum.GetFID(), datum.geometry().GetX(), datum.geometry().GetY())
			_p = _p.replace("{FLEXSPACE}", " "*(80 - (len(_p) - len("{FLEXSPACE}"))))
			print _p


if __name__ == '__main__':
	#main()
	filter_to_elora()
