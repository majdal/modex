import json
import simpacks.lightbulb 
from simpacks.lightbulb.lightbulb.working_lightbulb import Lamps, People 
import garlicsim
import modex

def run_lightbulb_sim(years, pop_size):
    lamps = Lamps()
    people = People(pop_size)
    interventions = [] # will add later
        
    start_light_data = {"Incandescent": [],
                        "CFL": [],
                        "Halogen": [],
                        "LED":[]}

    root_state = simpacks.lightbulb.state.State.create_root(lamps, people, interventions, start_light_data)

    return garlicsim.list_simulate(root_state, years)
   
def process_sim_data(results):
    raw_data = {"type_incandescent":[],
                      "type_halogen":[],
                      "type_cfl":[],
                      "type_led":[]}

    for result in results:
        year_data = vars(result)
        for field in year_data:
            if field in raw_data:
                raw_data[field].append(year_data[field])

    
    return raw_data

def get_lightbulb_json(years, pop_size=250):
    sim_results = run_lightbulb_sim(years, pop_size)    
    lightbulb_data  = process_sim_data(sim_results)

    event_type = "simulator"
    event_args = (years, pop_size)
    raw_json = [event_type, lightbulb_data, event_args]
    return json.dumps(raw_json)

if __name__ == "__main__":
    print get_lightbulb_json(10)

