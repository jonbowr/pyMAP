import simPyon as sim
from .esa_cs_const import *
from .cs import cs_scatterer
import os


class simulator:

    def __init__(self,geo = 'imap1'):
        inp = sim_input[geo].copy()
        inp['home'] = os.path.relpath(sim_input[geo]['home'])
        self.simion = sim.simion(**inp)
        for l,v in cs_locs[geo].items():
            self.simion.source.pos[l] = v
        self.scatterer = cs_scatterer()
        self.source = sim.particles.auto_parts()
        # se

    def splat_to_source(self,splat,source):
        inter_dist = {'ke':splat.df['ke'],
         'az':splat.df['phi']-180,
         'el':splat.df['theta'],
         'pos':np.stack([splat.df['x'],splat.df['r']]).T}
        for lab,val in inter_dist.items():
            source.df[lab] = sim.particles.source('fixed_vector',dist_vals = {'vector':val})

