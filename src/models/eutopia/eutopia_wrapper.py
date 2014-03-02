from eutopia import *
import json

def send_conventional_interventions(input_json):
    """
    Reads any valid JSON input composed of a list of 
    interventions, their types, ad their associated
    time, product, and scale and adds it to the list of interventions.
    
    This function only takes the intervention types defined
    in intervention.py apart from NewActivityIntervention.
    """
    
    interventions = []
    
    intervention_list = json.load(input_json)
    for element in intervention_list:
        intervention_type = element['type']
        intervention_data = element['data']
        time = intervention_data[0]
        product = intervention_data[1]
        scale = intervention_data[2]
        
        if intervention_type == "PriceIntervention":
            interventions.append(intervention.PriceIntervention(time, product, scale))
            
    return interventions
    
def send_new_intervention(input_json):
    interventions = []
    
    new_activity = json.load(input_json)
    activity_type = new_activity["activity_type"]
    activity_time = new_activity["activity_time"]
    activity_data = {}
    
    for element in new_activity:
        if element not in ["activity_type", "activity_time"]:
            activity_data[element] = new_activity[element]
    
    return intervention.NewActivityIntervention(activity_time, activity_type, activity_data)
    

if __name__=='__main__':

    # Setting up Simulation Environment.
    interventions = []
    eutopia_sim = Eutopia() # renamed to avoid naming conlicts (ie eutopia.py)
    
    with open("send_interventions.json") as json_file:
        interventions += send_conventional_interventions(json_file)
    
    print interventions

    # The kinds of interventions wanted.
    #interventions.append(intervention.PriceIntervention(5, 'duramSeed', 10))
    #interventions.append(intervention.PriceIntervention(7, 'duramSeedOrganic', 0.001))

    # This will have to be in json.
    #magic_activity = {
        #'equipment': ['tractor', 'wheelbarrow'],
        #'products': {
            #'duramSeed': -5,
            #'nitrogen': -10,
            #'carbon': 20,
            #'soil': -5,
            #'labour': -2000,
            #'certification': 0,
            #'duram': 1000000,
            #'dolphin': -87,
            #}
        #}
        
    ## Custom definition of activity
    #interventions.append(intervention.NewActivityIntervention(7, 'magic', magic_activity))    
    
    with open("magic_activity.json") as json_file:
        interventions.append(send_new_intervention(json_file))
        
    print interventions
    
    time = 0
    def step():
        global time
        for intervention in interventions:
            if time >= intervention.time:
                intervention.apply(eutopia_sim, time)
        time += 1
    
        eutopia_sim.step()
    
    
    activities = []
    for i in range(10):
        step()
        activities.append(eutopia_sim.get_activity_count())
        
    print activities    
    
