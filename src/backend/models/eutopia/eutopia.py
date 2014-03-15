#!/usr/bin/env python2
# this program requires python2 because GDAL requires python2

import os
from itertools import izip

from pygdal import *

import activity
import intervention


HERE = os.path.abspath(os.path.dirname(__file__))


#######################
## eutopia

MAP_SHAPEFILE = os.path.join(HERE, "Elora_esque.shp/") #not in the repo due to copyright; ask a team member


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


class Farm(Feature):
    def __init__(self, feature):
        Feature.__init__(self, feature)
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



class Eutopia:
    "The Eutopic World"
    "The main simulation class"
    ""
    "There is an API here for controlling and querying the model state"

    def __init__(self, log = None):
        self.log = log
        
        try:
            shapefile = Shapefile(MAP_SHAPEFILE)
        except IOError:       #py2.7
            #except FileNotFoundError: #py3k
            raise RuntimeError("No shapefile `%s` found; you may need to download it from a team member (privately)" % MAP_SHAPEFILE)

        self.map = shapefile[0] #cheating: assume the only layer we care about is this one
        assert self.map.GetGeomType() == wkbPolygon, "Farm boundaries layer is not a Polygon; it is a" + str.join(" or ", invertOGRConstants(self.map.GetGeomType()))
        #assert isinstance(self.map, PolygonLayer), "Farm boundaries layer is not a Polygon; it is a " + str(type(self.map))

        #########################
        # modelling begins here
        self.time = 0
        self.activities = activity.Activities()
        self.interventions = []

        #XXX should we write this as literally constructing a new Layer?
        # for now, a List is alright, but it's worth thinking about doing that and about what pygdal requires to support doing that
        self.farms = [Farm(f) for f in self.map if f.MAP_CODE in AGRICULTURE_CODES.keys()]
        print("Constructed", len(self.farms), "farms", "out of", len(self.map), "features")

        self.families = []
        # for now, every Family goes with one single Farm on it
        for farm in self.farms:
            family = FarmFamily(self)
            family.add_farm(farm)
            self.families.append(family)

    def dumpMap(self):
        "convert the map data to GeoJSON"
        "meant to be used in a ModelExplorer endpoint"
        return self.map.dumps()

    def __next__(self):
        # apply interventions
        for intervention in self.interventions:
            if self.time >= intervention.time:
                intervention.apply(self, self.time)
        
        # run model
        for family in self.families:
            family.step()
        self.time += 1
        
        # log metrics
        if self.log is not None:
            self.log.append((self.time, self.get_activity_count())) #XXX assumes a list (or a list-like object)
    
    next = __next__ #py2 :(
    step = __next__ #backwards compat
    
    def intervene(self, intervention):
        self.interventions.append(intervention)

    def __iter__(self):
        "convenience method"
        while True:
            next(self)
            yield self.get_activity_count() #hardcode model output, for now

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
    n = 10 #number of steps to run
           #TODO: make this a command line param
    
    log = []
    eutopia = Eutopia(log)

    eutopia.intervene(intervention.PriceIntervention(5, 'duramSeed', 10))
    eutopia.intervene(intervention.PriceIntervention(7, 'duramSeedOrganic', 0.001))

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
    eutopia.intervene(intervention.NewActivityIntervention(7, 'magic', magic_activity))
    
    #run the model
    for i in range(n):
        next(eutopia)
    
    activities = [state for time, state in log]
    print activities

    # optional:
    #write a geojson file containing the loaded map dataset
    #with open("elora.geo.json","w") as mapjson:
    #    mapjson.write(eutopia.dumpMap())

    # optional: display summary of model outputs
    #import pylab
    #pylab.plot(range(len(activities)), [a.get('durumWheatConventional',0) for a in activities])
    #pylab.plot(range(len(activities)), [a.get('durumWheatGreen',0) for a in activities])
    #pylab.plot(range(len(activities)), [a.get('magic',0) for a in activities])
    #pylab.show()
