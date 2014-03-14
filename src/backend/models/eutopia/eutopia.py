
import os, zipfile
import ogr #GDAL's vector library
ogr.UseExceptions() #make ogr sane

AGRICULTURE_CODES = { #hardcoded out of the ARI dataset
   #non-agriculture features are commented out
   'C': 'CORN SYSTEM',
   #'B': 'BUILT UP',
   'G': 'GRAZING SYSTEM',
   'PC': 'PEACHES-CHERRIES',
   'H': 'HAY SYSTEM',
   'M': 'MIXED SYSTEM',
   'MG': 'GRAIN SYSTEM',
   'KM': 'MARKET GARDENS/TRUCK FARMS',
   'KN': 'NURSERY',
   'P': 'CONTINUOUS ROW CROP',
   #'A1': 'IDLE AGRICULTURAL LAND (5-10 YEARS)',
   #'A2': 'IDLE AGRICULTURAL LAND (OVER 10 YEARS)',
   #'W': 'WATER',
   #'X': 'SWAMP, MARSH OR BOG',
   #'R': 'RECREATION',
   #'Z': 'WOODLAND',
   #'E1': 'EXTRACTION PITS AND QUARRIES',
   #'HG': 'PASTURE SYSTEM',
   #'ZR': 'REFORESTATION'  
}

ogr.CONSTANTS = dict((e, ogr.__dict__[e]) for e in ogr.__dict__.keys() if e.startswith("wkb"))

def invertOGRConstant(value):
    "given a value, find the names of the constants that goes with it"
    "i'm sorry; this is really just a quick hack for debugging and should be replaced by wrapping the OGR constants in enum objects"
    return [n for n in ogr.CONSTANTS if ogr.CONSTANTS[n] == value]

import activity
import intervention

import os
HERE = os.path.abspath(os.path.dirname(__file__))
MAP_SHAPEFILE = os.path.join(HERE, "Elora_esque.shp.zip") #not in the repo due to copyright; ask a team member

class Geometry(object):
    "a simple wrapper that makes OGR objects pythonic"
    "every row in the table is exposed as a property"
    def __init__(self, ogr_feature):
        assert isinstance(ogr_feature, ogr.Feature)
        self.__dict__['fields'] = ogr_feature #speak to __dict__ directly here because of dirty __getattr__ magic
        self.__dict__['geometry'] = ogr_feature.GetGeometryRef()
        
    def __getattr__(self, name):
        print "getattr(", id(self), "," , name, ")"
        assert ogr.GetUseExceptions() == True, "This code depends on GDAL mapping error codes to exceptions for us"
        # check: local dict, then the fields (we can't access self.fields without accessing the local dict) and only then call up
        try:
            print("I AM THE BASTER MASTER", name)
            return self.__dict__[name] #whyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
        except:
            # darn
            # this causes infinite regress
            try:
                return self.fields.GetField(name)
            except:
                print("MAJOR FAILE.")
                raise
                #return getattr(self, name) #this causes infintie loop

            #return object.__getattribute__(self, name) #very python2...  <http://stackoverflow.com/questions/3278077/difference-between-getattr-vs-getattribute-in-python>
    
    def __setattr__(self, name, value):
        assert ogr.GetUseExceptions() == True, "This code depends on GDAL mapping error codes to exceptions for us"
        try:
            return self.fields.SetField(name, value) #this causes infinite regress because it calls self.fields which triggers getattr
        except RuntimeError: #ogr gives this for all errors when UseExceptions() is on
            return object.__setattr__(self, name, value)
    
class Farm(Geometry):
    def __init__(self, feature):
        Geometry.__init__(self, feature)
        #self.land_type = land_type #hmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        self.county = "BestCountyInTheWorldIsMyCountyAndNotYours"
        
        self.last_activity = None
    
    #backwards compat
    @property
    def id(self): return self.fields.GetFID()

    @property
    def lat(self): return self.geometry.Centroid().GetY()

    @property
    def long(self): return self.geometry.Centroid().GetX()

    @property
    def area(self): return self.geometry.Area()


class FarmFamily:
    def __init__(self, eutopia):
        self.eutopia = eutopia
        self.farms = []
        self.bank_balance = 1000000.00
        self.equipment = []
        self.preferences = {'money': True}
        
    def add_farm(self, farm):
        self.farms.append(farm)
        farm.family = self
        
    def make_planting_decision(self, activities, farm):    
        best = None
        for activity in activities:
            total = 0
            for pref, weight in self.preferences.items():
                total += activity.get_product(pref, farm) * weight
                # TODO: improve choice algorithm
                #    - maybe by allowing different sensitivities to risk
                #      on different income dimensions
                
            if best is None or total > best_total:
                best = activity
                best_total = total
        
        return best        
        
    
    def step(self):
        for farm in self.farms:
            # changed to self.eutopia to make it work with the sim version that is passed to Family21
            activity = self.make_planting_decision(self.eutopia.activities.activities, farm)
            
            money = activity.get_product('money', farm)
            self.bank_balance += money
            
            farm.last_activity = activity


#TODO: move the map stuff into class Map
# add a .dumps() method

class Eutopia:
    def __init__(self):
        if zipfile.is_zipfile(MAP_SHAPEFILE):
            #the logic here should be:
            # check if zipfile, if so unzip and continue as if that didn't happen
            #  check if folder; if so, check if ogr can read it
            #  otherwise, check if ogr can read it
            # but that cleanliness can come in PyGDAL (or maybe by snitching code from QGIS? actually, doesn't QGIS use GDAL? ..do they have PyGDAL written, or are they just using the SWIG interface?)

            # unzip the shapefile in almost the most sketchy way possible
            SHAPEFILE = MAP_SHAPEFILE.replace(".zip","") #XXX sketchy
            os.system("rm -r '%s'" % (SHAPEFILE,)) #XXX sketchy
            os.system("unzip -d '%s' '%s'" % (SHAPEFILE, MAP_SHAPEFILE)) #XXX sketchy
        else:
            raise RuntimeError("No shapefile `%s` found; you may need to download it from a team member (privately)" % MAP_SHAPEFILE)
        """"""
        shapefile = ogr.Open(SHAPEFILE) 
        self.map = shapefile.GetLayer(0) #cheating
        self.map._source = shapefile #stash shapefile to make sure it dooesn't get freed before Map does
        assert self.map.GetGeomType() == ogr.wkbPolygon, "Farm boundaries layer is not a wkbPolygon layer; it is a" + str.join(" or ", invertOGRConstants(self.map.GetGeomType()))
        
        self.time = 0
        
        self.activities = activity.Activities()
        
        def features(layer): #todo factor this _hard_
            for i in range(layer.GetFeatureCount()):
                yield layer.GetFeature(i)
        self.farms = [Farm(f) for f in features(self.map) if f.MAP_CODE in AGRICULTURE_CODES.keys()]
        print("Constructed", len(self.farms), "farms", "out of", self.map.GetFeatureCount(), "features")
        
        self.families = []
        for farm in self.farms:
            family = FarmFamily(self)
            family.add_farm(farm)
            self.families.append(family)
            
    def step(self):
        for family in self.families:
            family.step()
        self.time += 1
    
    def __iter__(self):
        while True:
            self.step()
            yield
            
    def get_activity_count(self):
        activities = {}
        for farm in self.farms:
            if farm.last_activity is not None:
                name = farm.last_activity.name
                if name not in activities:
                    activities[name] = 1
                else:
                    activities[name] += 1
        return activities            
                
        
if __name__=='__main__':
    

    eutopia = Eutopia()

    interventions = [intervention.PriceIntervention(5, 'duramSeed', 10), 
                     intervention.PriceIntervention(7, 'duramSeedOrganic', 0.001)]
    
    magic_activity = {
        'equipment': ['tractor', 'wheelbarrow'],
        'products': {
            'duramSeed': -5,
            'nitrogen': -10,
            'carbon': 20,
            'soil': -5,
            'labour': -2000,
            'certification': 0,
            'duram': 1000000,
            'dolphin': -87,
            }
        }
    interventions.append(intervention.NewActivityIntervention(7, 'magic', magic_activity))    
    
    
    time = 0
    def step():
        global time
        for intervention in interventions:
            if time >= intervention.time:
                intervention.apply(eutopia, time)
        time += 1
    
        eutopia.step()
    
    
    activities = []
    for i in range(10):
        step()
        activities.append(eutopia.get_activity_count())
    
    print activities
    
    #import pylab
    #pylab.plot(range(10), [a.get('durumWheatConventional',0) for a in activities])
    #pylab.plot(range(10), [a.get('durumWheatGreen',0) for a in activities])
    #pylab.plot(range(10), [a.get('magic',0) for a in activities])
    #pylab.show()

        
