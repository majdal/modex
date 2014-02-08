class Product:
    def __init__(self, product_data):
        """
        This will take in values from a .csv file
        or database and assign them to several values.
        """
        self.name = product_data["name"]
        self.market_price = float(product_data["market_price"])
        self.seed_cost = float(product_data["seed_cost"])
        self.labor_cost = float(product_data["labor_cost"])
        self.fertilizer_cost = float(product_data["fertilizer_cost"])

        self.subsidies = {}

    def get_price(self):
        return self.market_price

    def get_total_cost(self):
        """
        get_total_cost combines all the factors of 
        cost data and obtains an average (unit price
        per season cost) for a particular Product.
        """
        
        return self.seed_cost + self.labor_cost + self.fertilizer_cost 

    def calculate_profit(self):
        return self.get_price() - self.get_total_cost() 

class Externality:
    def __init__(self):
        self.name = ""

        self.rate = 1

        self.boundary_values = []

class Tax(Externality):
    def __init__(self):
        pass

class Subsidy(Externality):
    def __init__(self):
        pass

class Policy(Externality):
    def __init__(self):
        pass

class Farmer():
    def __init__(self):
        self.name = ""
        self.capital_assets = [] # tractors/farmhouses/etc
        self.cash = 0

    def make_decision(self):
        pass
