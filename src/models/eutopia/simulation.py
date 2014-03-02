from intervention import PriceIntervention, NewActivityIntervention
from eutopia import *
import json

class Scenario:
    def __init__(self, interventions):
        self.interventions = interventions
        
class Simulation:
    def __init__(self):
        self.scenarios = {}

def read_interventions(interventions):
    """
    Reads a json file with the format:
    [ {'name':, 'type':, 'data':[], 'simulation':,}
    ...
    ]
    and returns a simulation object, which in turn contains
    a dict of scenario objects, which each contain Intervention objects
    """
    
    simulation = Simulation()
    
    for intervention in interventions:
        scenario = intervention["scenario"]
        data = intervention["data"]
        
        if intervention["type"] == "priceIntervention":
            intervention_obj = PriceIntervention(*data)
        
        elif intervention["type"] == "newActivityIntervention":
            intervention_obj = NewActivityIntervention(*data)
        
        
        if simulation.scenarios.has_key(scenario):
            simulation.scenarios[scenario].append(intervention_obj)
            
        else:
            simulation.scenarios[scenario] = [intervention_obj]
            
    return simulation
    

        
if __name__ == "__main__":
    eutopia = Eutopia()
    
    with open("interventions.json", "r") as input_json:
        interventions_json = json.load(input_json)
    
    simulation = read_interventions(interventions_json)
    interventions = simulation.scenarios[1] # indexed by scenario 1
    
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
        print eutopia.get_activity_count() # this is on a year to year basis.
        
    print activities    
        
    
        
        
    
