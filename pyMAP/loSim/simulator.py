import simPyon as sim
from .esa_cs_const import *
from .cs import cs_scatterer
import os


class simulator:
    '''
    Structure requirements for usage a sim node:
    - kind: string catagorizing the simulation type
    - fly(): function which executes particle propagation
    '''

    def __init__(self,geo = 'imap1'):
        inp = sim_input[geo].copy()
        inp['home'] = os.path.relpath(sim_input[geo]['home'])
        from pandas import DataFrame
        self.sims = DataFrame([\
                    {'name':'inc_N',
                        'kind':'simion',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['CS']),
                                },
                    {'name':'cs_scatter',
                        'kind':'modulator',
                        'sim':cs_scatterer(),
                                },
                    {'name':'rec_ion',
                        'kind':'simion',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['TOF']),
                                }
                    ]).set_index(['name','kind'])['sim']
        # self.sims = {'inc_N':{'sim':sim.simion(**inp,
        #                             obs_region = obs_regions['CS']),
        #                         'kind':'simion',
        #                         'order':1,
        #                         },
        #             'cs_scatter':{'sim':cs_scatterer(),
        #                             'kind':'modulator',
        #                             'order':2,
        #                         },
        #             'rec_ion':{'sim':sim.simion(**inp,
        #                             obs_region = obs_regions['TOF']),
        #                         'kind':'simion',
        #                         'order':3,
        #                         }
        #             }
        self.source = sim.particles.auto_parts()
        self.source['charge'] = 0
        self.source['ke'] = sim.particles.source('gaussian')
        self.source['ke'].dist_vals = {'mean': 930, 'fwhm': 50}
        self.source['az'].dist_vals = {'mean': 180, 'fwhm': 2}
        self.source['el'].dist_vals = {'mean': 0,'fwhm': 2}
        self.source['pos'].dist_vals = {'first': np.array([210, 119.2,   0. ]), 
                                    'last': np.array([210.1,133.2,   0. ])}
        self[0].source = self.source
        # for sm in self.sims:
        #     for l,v in cs_locs[geo].items():
        #         if self.sims[sm]['kind'] =='simion':
        #             self.sims[sm]['sim'].source['pos'][l] = v
            
    def __getitem__(self,item):
        return(self.sims[item])

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
                dat_buffer = vals['sim'].data.stop()
                self.dat[lab] = vals['sim'].data
            elif vals['kind']=='modulator':
                dat_buffer = vals['sim'].fly(dat_buffer)
                self.dat[lab] = dat_buffer

    def fly_trajectory(self,n = 100):
        from matplotlib import pyplot as plt
        self.source['n'] = n
        self.fly(n)
        for lab,vals in self.sims.items():
            if vals['kind'] == 'simion':
                if vals['order']==1:
                    fig,ax = vals['sim'].show()
                vals['sim'].source.splat_to_source(vals['sim'].data.start())                    
                try:
                    vals['sim'].fly_trajectory(cores = 1,fig = fig,ax = ax,show_cbar = False)
                except: Pass
