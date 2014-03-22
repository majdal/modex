"""
eutopia: framework for simulating possible worlds of agriculture in Southern Ontario.
"""

# eutopia.py is king in this module
# so we export everything that eutopia.py exports
from .eutopia import *

# but the real power lies in the queen: simulation.py.
# Currently it is a member of this module, but Simulation
# should be pulled out of this module once it (and Eutopia 
# (and server.py)) is generic enough.
from .simulation import *

# now, we explicitly hide the irrelevant helper modules
# from "from eutopia import *" lines:
__all__   =  []
__all__  +=  eutopia.__all__ 
__all__  +=  simulation.__all__
