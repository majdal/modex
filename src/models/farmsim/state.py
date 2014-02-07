from econ_model.definitions import Product, Farmer
from econ_model import farmer_finance
import garlicsim.data_structures
import modex

log = modex.log()

class State(garlicsim.data_structures.State,):
    def __init__(self, farmer, products_list, y=0):
        garlicsim.data_structures.State.__init__(self)

        self.farmer = farmer # farmer object
        self.products = products_list # product objects
        self.y = y # years, steps in quarters

    def step(self):
        
        # simple seasons
        for q in xrange(0,4):
            current_profit = 0
            for item in self.products:
               current_profit += item.calculate_profit() 
        
        self.farmer.cash += current_profit
         
        log.time = self.y
        log.current_cash = self.farmer.cash

        self.y += 1
        return State(self.farmer, self.products, self.y)
    
        
    @staticmethod
    def create_root(farmer, products_list):
        return State(farmer, products_list)


if __name__ == "__main__":
    start_farmer = Farmer()
    start_products = farmer_finance.get_products()
    start_state = State.create_root(start_farmer, start_products)
    garlicsim.simulate(start_state, 5)
