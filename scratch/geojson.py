# geojson.py
# 
# ---copyright goes here---
# this is python2 code

#Allaura is at:
#  -80.25.38, 43.41.6    and a 200by200km area   near 43 latitude one degree longitude is roughly 100km one degree lat is 83km
#  -80.42722 , 43.685
# 

import osgeo.ogr as ogr
import geojson

shapefile = "../assets/maps/_ags_DMTI_2010_CanMapRL_POI_AER_ALL_PROV2"
#shapefile = "../assets/maps/OGDE_ARI/AgricultureResourceInventory_1983"

import IPython
IPython.terminal.embed.TerminalInteractiveShell.confirm_exit=False #i want
#IPython.get_config().InteractiveShell.confirm_exit = False

def main():
	"for debugging"
	dataset = ogr.Open(shapefile)
	print ("Loaded it, yo")
	raw_input();
	for l in range(dataset.GetLayerCount()):
		layer = dataset.GetLayerByIndex();
		print layer.GetName(), "has these coordinates", layer.GetExtent()
		print "which are relative to this reference:"
		print str(layer.GetSpatialRef())
		for f in range(layer.GetFeatureCount()):
			datum = layer.GetFeature(f)
			#IPython.embed(); break;
			#print datum.keys()
			#MAP_DESCR
			_p = "%s, %s{FLEXSPACE}(%.3f, %.3f)" % (datum['name'], datum['city'], datum.geometry().GetX(), datum.geometry().GetY())
			#_p = "FID%d:{FLEXSPACE}(%.3f, %.3f)" % (datum.GetFID(), datum.geometry().GetX(), datum.geometry().GetY())
			_p = _p.replace("{FLEXSPACE}", " "*(80 - (len(_p) - len("{FLEXSPACE}"))))
			print _p
			
			#time.sleep(2)
			#break


if __name__ == '__main__':
	main()
