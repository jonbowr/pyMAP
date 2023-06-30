import simPyon as sim
from .esa_cs_const import *
from .cs import cs_scatterer
import os
import pandas as pd

class simulator:
    '''
    Structure requirements for usage a sim node:
    - kind: string catagorizing the simulation type
    - fly(): function which executes particle propagation
    '''

    def __init__(self,geo = 'imap1',scattering_input = {}):
        inp = sim_input[geo].copy()
        inp['home'] = os.path.relpath(sim_input[geo]['home'])
        from pandas import DataFrame
        # setup the simulator architecture
        self.sims = DataFrame([\
                    {'name':'inc_N',
                        # 'kind':'simion',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['CS']),
                                },
                    {'name':'cs_scatter',
                        # 'kind':'modulator',
                        'sim':cs_scatterer(**scattering_input),
                                },
                    {'name':'rec_ion',
                        # 'kind':'simion',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['TOF']),
                                }
                    ]).set_index(['name'])['sim']

        # setup the default source distribution
        self.source = sim.particles.auto_parts()
        self.source['charge'] = 0
        self.source['ke'] = sim.particles.source('gaussian')
        self.source['ke'].dist_vals = {'mean': 930, 'fwhm': 50}
        self.source['az'].dist_vals = {'mean': 180, 'fwhm': 2}
        self.source['el'].dist_vals = {'mean': 0,'fwhm': 2}
        self.source['pos'].dist_vals = {'first': np.array([210, 119.2,   0. ]), 
                                    'last': np.array([210.1,133.2,   0. ])}

        # setup param control structure for easy access to sub simulation adjustable params
        self.params = {}
        # self.params['source'] = self.source.params
        self.params['cs_scatter'] = self['cs_scatter'].params

    def __repr__(self):
        return(
               'Simulator Nodes:\n'+
               'Source:%s'%str(self.source)+
               '====================================\n'+
                '====================================\n'.join(\
                ['%s:%s'%(lab[0],str(val))for lab,val in self.sims.items()]))
            
    def __getitem__(self,item):
        return(self.sims[item])

    def __setitem__(self,item,val):
        self.sims[item]=val
        return(self)
    

    def show(self):
        return(self[0].show())

    def sim_fix_stops(self,data,v_extrap = True):
        # uses the shapely instrument geometry to set points on surface of polygon
        #   to prevent pixlization collisions on reinitialization using collision locs
        from shapely.geometry import MultiPoint
        from shapely.ops import nearest_points
        pol = self[0].geo.get_single_poly().boundary

        pts = MultiPoint(data[['x','r']])
        verts = np.array([[pr.x,pr.y] for pr in [nearest_points(pol,pt)[0] for pt in pts.geoms]])
        if v_extrap:
            #calc offset distance of point from surface
            mm_offset = np.sqrt((data['x'] -verts[:,0])**2+(data['r'] - verts[:,1])**2)
            # step the particles backward according to offset distance
            #    in trajectory based on their velocity
            for dim in ['x','r']:
                data[dim] = data[dim]-data['v'+dim]/abs(data['v'+dim])*mm_offset
            pts = MultiPoint(data[['x','r']])
            verts = np.array([[pr.x,pr.y] for pr in [nearest_points(pol,pt)[0] for pt in pts.geoms]])
        data['x'] = verts[:,0]
        data['r'] = verts[:,1]
        return(data)

    def fly(self,n = 1000,quiet = True):
        self.source['n'] = n
        dat_buffer = self.source.copy()
        for lab,sim_in in self.sims.items():
            dat = sim_in.fly(dat_buffer,quiet = quiet).good().stop()
            if 'counts' in dat_buffer.df:
                try:
                    sim_in.data.append_col(dat_buffer['counts']*sim_in.data.start()['counts'],'counts')
                except:
                    Warning('Count Propagation failed: Most likely incorrect Ion initialization')
            if sim_in.type == 'simion':
                if len(dat)>0:
                    dat_buffer = self.sim_fix_stops(dat.copy())
            else:
                dat_buffer = dat.copy()
        return(self)

    def fly_trajectory(self,n = 100,fig = None,ax = None):
        from matplotlib import pyplot as plt
        self.source['n'] = n
        self.fly(n)
        if ax == None:
            fig,ax = self.show()
        for sim_in in self.sims:
            if sim_in.type == 'simion':
                sim_in.fly_trajectory(len(sim_in.data.start().df),fig = fig,ax =ax,show_cbar = False)