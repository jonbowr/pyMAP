import simPyon as sim
from .esa_cs_const import *
from .cs import cs_scatterer


class simulator:

    __init__(self,geo = 'imap1'):
        self.simion = sim.simion(**sim_input[geo])
        for l,v in cs_locs[geo].items():
            sm.parts.pos[l] = v
        self.scatterer = cs_scatterer()

