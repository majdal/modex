import unittest


# Here's our "unit tests".
class LightbulbCase(unittest.TestCase):

    def test_init(self):
    	import sys
    	import os
    	cwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    	sys.path.append(cwd)
    	
    	#import ipdb; ipdb.set_trace()

    	from lightbulb.lightbulb import People, Lamps, Intervention
    	import lightbulb_simpack
    	import garlicsim

    	lamps = Lamps()
    	people = People(250)
    	interventions = []
    	data = {'Incandescent': [],
                'CFL': [],
                'Halogen': [],
                'LED': [],
                'time': []
        }
    	state = lightbulb_simpack.State.create_root(Lamps, people, interventions, data)
    	garlicsim.simulate(state)


if __name__ == '__main__':
    unittest.main()