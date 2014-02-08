import garlicsim.data_structures
import modex

log = modex.log()

# Note that modex is imported from 2 higher level directories.

class State(garlicsim.data_structures.State):
    # This is your `State` subclass. Your state objects should contain all the
    # information there is abolog = modex.log()ut a moment of time in your simulation.
    
    def __init__(self, start_lamps, start_people, start_interventions, light_data, y=0):
        """
        start_lamps: instance of lightbulb.Lamps
        start_people: instance of lightbulb.People 
        start_intervention: list of lightbulb.Intervention 
        light_data: Where the data will be saved. A dictionary of the form: { 'Incandescent': [],
                                     'CFL': [], 
                                     'Halogen': [],
                                     'LED': [],
                                     'time': []
                                     }
        """

        garlicsim.data_structures.State.__init__(self)

        self.type_incandescent = light_data["Incandescent"]
        self.type_cfl = light_data["CFL"]
        self.type_halogen = light_data["Halogen"]
        self.type_led = light_data["LED"]
        
        self.interventions = start_interventions

        self.lamps = start_lamps
        self.people = start_people
        self.interventions = start_interventions
        self.y = y

    
    def step(self):
        self.type_incandescent = self.people.get_count(type='Incandescent')
        self.type_cfl = self.people.get_count(type='CFL')
        self.type_halogen = self.people.get_count(type='Halogen')  
        self.type_led = self.people.get_count(type='LED')

        for w in range(52):
            self.people.step()
            #import ipdb; ipdb.set_trace()
            self.lamps.step()
            for interv in self.interventions:
                interv.step()

        log.time = self.y
        log.count_incandescent = self.type_incandescent
        log.count_cfl = self.type_cfl
        log.count_halogen = self.type_halogen
        log.count_led = self.type_led

        self.y += 1
        new_light_data = {"Incandescent": self.type_incandescent,
                          "CFL": self.type_cfl, 
                          "Halogen":self.type_halogen,
                          "LED": self.type_led}
    
        new_state = State(self.lamps, self.people, self.interventions,
                          new_light_data, self.y)
        
        return new_state
    
        
    @staticmethod
    def create_root(lamp, people, interventions, start_light_data):
        return State(lamp, people, interventions, start_light_data)


