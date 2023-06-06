import simPyon as sim
from .esa_cs_const import *
from .cs import cs_scatterer
import os


class simulator:

    def __init__(self,geo = 'imap1'):
        inp = sim_input[geo].copy()
        inp['home'] = os.path.relpath(sim_input[geo]['home'])

        # self.sims = {'inc_N':sim.simion(**inp,
        #                             obs_region = obs_regions['CS']),
        #             'cs_scatter':cs_scatterer(),
        #             'rec_ion':sim.simion(**inp,
        #                             obs_region = obs_regions['TOF']),
        #             }

        self.sims = {'inc_N':{'sim':sim.simion(**inp,
                                    obs_region = obs_regions['CS']),
                                'kind':'simion',
                                'order':1,
                                },
                    'cs_scatter':{'sim':cs_scatterer(),
                                    'kind':'modulator',
                                    'order':2,
                                },
                    'rec_ion':{'sim':sim.simion(**inp,
                                    obs_region = obs_regions['TOF']),
                                'kind':'simion',
                                'order':3,
                                }
                    }
        self.source = sim.particles.auto_parts()
        self.source['charge'] = 0
        self.source['ke'] = sim.particles.source('gaussian')
        self.source['ke'].dist_vals = {'mean': 930, 'fwhm': 50}
        self.source['az'].dist_vals = {'mean': 180, 'fwhm': 2}
        self.source['el'].dist_vals = {'mean': 0,'fwhm': 2}
        self.source['pos'].dist_vals = {'first': np.array([210, 119.2,   0. ]), 
                                    'last': np.array([210.1,133.2,   0. ])}
        for sm in self.sims:
            for l,v in cs_locs[geo].items():
                if self.sims[sm]['kind'] =='simion':
                    self.sims[sm]['sim'].source['pos'][l] = v
            
    def show(self):
        return()

    def fly(self,n = 1000):
        self.source['n'] = n
        self.dat = {}
        for lab,vals in self.sims.items():
            if vals['kind'] == 'simion':
                if vals['order']==1:
                    vals['sim'].source = self.source
                else:
                    vals['sim'].source.splat_to_source(dat_buffer)  
                vals['sim'].fly()
                dat_buffer = vals['sim'].data.good().stop().df
                self.dat[lab] = vals['sim'].data
            elif vals['kind']=='modulator':
                dat_buffer = vals['sim'].fly(dat_buffer)


    def fly_trajectory(self,n = 100):
        from matplotlib import pyplot as plt

        self.source['n'] = n
        self.fly()
        for lab,vals in self.sims.items():
            if vals['kind'] == 'simion':
                if vals['order']==1:
                    vals['sim'].source = self.source
                    fig,ax = vals['sim'].show()
                else:
                    vals['sim'].source.splat_to_source(dat_buffer)
                vals['sim'].fly_trajectory(fig = fig,ax = ax)
                dat_buffer = vals['sim'].data.stop().df
            elif vals['kind']=='modulator':
                dat_buffer = vals['sim'].fly(dat_buffer)
