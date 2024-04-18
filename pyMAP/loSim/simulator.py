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

    def __init__(self,config = 'imap',mode = 'imap_hiTh',estep = 6,
                                scattering_input = {}):
        inp = sim_input(config,mode,estep)
        inp['home'] = os.path.relpath(inp['home'])

        lpath = os.path.dirname(__file__)
        gemPath = os.path.join(lpath,'/IMAP-Lo_CR7_CE13_TOF2_HK6')

        
        from pandas import DataFrame
        # setup the simulator architecture
        self.config = config
        self.mode = mode
        self.sims = DataFrame([\
                    {'name':'inc_N',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['CS']),
                                },
                    {'name':'cs_scatter',
                        'sim':cs_scatterer(**scattering_input),
                                },
                    {'name':'rec_ion',
                        'sim':sim.simion(**inp,
                                obs_region = obs_regions['TOF']),
                                }
                    ]).set_index(['name'])['sim']
        self.geo = self.sims['inc_N'].geo
        self.sims['cs_scatter'].geo = self.geo

        # setup the default source distribution
        self.source = sim.particles.auto_parts()
        self.source['charge'] = 0
        self.source['ke'] = sim.particles.source('gaussian')
        self.source['ke'].dist_vals = {'mean': 480*volt_scale_facts[estep-1], 'fwhm': 50*volt_scale_facts[estep-1]}
        self.source['az'].dist_vals = {'mean': 180, 'fwhm': 2}
        self.source['el'].dist_vals = {'mean': 0,'fwhm': 2}
        self.source['pos'].dist_vals = {'first': np.array([210, 119.2,   0. ]), 
                                    'last': np.array([210.1,133.2,   0. ])}
        self.sims[0].source = self.source.copy()

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
        fig,ax = self[0].show()
        from matplotlib.patches import Rectangle
        for s in self.sims:
            if s.type == 'simion':
                sr = s.obs_region
                ax.add_patch(Rectangle((sr['X_MIN'], sr['R_MIN']), 
                                       sr['X_MAX']-sr['X_MIN'], 
                                       sr['R_MAX']-sr['R_MIN'],linewidth=1, 
                                       edgecolor='r', facecolor='none'))
        return(fig,ax)

    def show_dist(self):
        self.sims.apply(lambda x: x.data.start().show())

    def fast_adjust(self,scale_fact = 1,
                            estep = None,
                                mode = 'imap_hiTh',
                                up_un = None):
        if up_un is not None:
            v_nom = self.__set_upos_uneg__(*up_un)
        elif estep is not None:
            v_nom = v_modes().loc[mode][estep]
        else:
            v_nom = dict(self[0].volt_dict)
        for i in [0,2]:
            self[i].volt_dict = dict(v_nom)
        self[0].fast_adjust(scale_fact = scale_fact)
        return(self)

    def __set_upos_uneg__(self,upos ,uneg):
        thing = {'u+':upos,'u-':uneg}
        v_nom = v_modes().loc['imap_hiTh'][7]
        v_out = dict(v_nom)
        volt_setter = pd.DataFrame({'u':['u+','u-'],
                               'elec':['P10 Electrode','P2 Electrode'],
                              'elecs':[['Inner ESA','P10 Electrode'],
                                      ['Conversion Surface','P2 Electrode','P9 Electrode']]})
        new_volts = volt_setter.apply(lambda x: v_nom[x['elecs']]/v_nom[x['elec']]*thing[x['u']],axis = 1).stack().reset_index(0,drop = True)
        for lab,v in new_volts.items():
            v_out[lab] = v
        for i in [0,2]:
            self[i].volt_dict = v_out
        return(v_out)

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

    def __fly_buff__(self,sim_in,dat_buffer,quiet = True):
        dat = sim_in.fly(dat_buffer,quiet = quiet).stop()
        if 'counts' in dat_buffer.df:
            try:
                sim_in.data.append_col(dat_buffer['counts']*sim_in.data.start()['counts'],'counts')
            except:
                Warning('Count Propagation failed: Most likely incorrect Ion initialization')
        if sim_in.type == 'simion':
            if len(dat)>0:
                return(sim_in.fix_stops(dat.copy(),v_extrap = True,buffer = .025,mm_offset = .025))
        else:
            return(dat.copy())

    def fly(self,n = 1000,quiet = True,leg = 'all'):
        if leg == 'all':
            steps = range(len(self.sims))
        elif type(leg)==int:
            steps = range(leg,leg+1)
        else:
            steps = leg

        if leg ==0 or leg == 'all':
            self.source['n'] = n
            dat_buffer = self.source.copy()
        else:
            if self[steps[0]-1].type == 'simion':
                dat_buffer = self[steps[0]-1].fix_stops(self[steps[0]-1].data.stop(),
                                            v_extrap = True,buffer = .025,mm_offset = .025)
            else:
                dat_buffer = self[steps[0]-1].data.stop()

        for lab,sim_in in self.sims[steps].items():
            dat_buffer = self.__fly_buff__(sim_in,dat_buffer,quiet = quiet)
        return(self)

    def fly_trajectory(self,n = 100,fig = None,ax = None):
        from matplotlib import pyplot as plt
        self.source['n'] = n
        self.fly(n)
        if ax == None:
            fig,ax = self.show()
        for sim_in in self.sims:
            if sim_in.type == 'simion':
                sim_in.fly_trajectory(sim_in.data.start(),fig = fig,ax =ax,show_cbar = False)
        return(fig,ax)

    def get_data(self):
        return(splats(self.sims.apply(lambda x: x.data.copy())))

    def get_good(self,dat,leg = 0):
        #filter each data set step for one data set being good, assumes all data have exact same size
        def good_app(x):
            new_dat = x.copy()
            new_dat.df = new_dat.df.set_index('ion n').loc[dat[leg].good().start().df['ion n'].values].reset_index()
            return(new_dat)
        return(dat.apply(good_app))


class splats:
    def __init__(self,dats):
        self.dfs = dats
        
    def __getitem__(self,item):
        return(self.dfs[item])
    
    def __setitem__(self,item,value):
        self.dfs[item] = value
    
    def start(self):
        return(dat.apply(lambda x:x.start()))

    def get_good(self,leg = 0):
        #filter each data set step for one data set being good, assumes all data have exact same size
        def good_app(x):
            new_dat = x.copy()
            new_dat.df = new_dat.df.set_index('ion n').loc[self[leg].good().start().df['ion n'].values].reset_index()
            return(new_dat)
        
        return(splats(self.apply(good_app)))

    def get_loc(self,ion_nums):
        def locr(dat,ion_nums):
            new_dat = dat.copy()
            new_dat.df = new_dat.df.set_index('ion n').loc[ion_nums].reset_index()
            return(new_dat)
        return(splats(self.apply(lambda x: locr(x,ion_nums))))
    
    def apply(self,func):
        return(self.dfs.apply(func))
    
    def show(self,params = {}):
        return(self.apply(lambda x: x.show(**params)))
    
    def start(self):
        return(splats(self.apply(lambda x: x.start())))

    def calc_count_rate(self,inc_flux = 10000,pac_kv = 10,ap_window = 2.6,):
        '''
        ONLY for H right now
        inc_flux: cts/sec/cm^2
        pac_kv: pav_voltage in kV
        ap_window: illuminated area in cm^2
        '''
        def effic_tof_H(pac_kv = 10):
            # TOF trip effic taken from TOFCal
            m = .019
            b = .140
            return(m*pac_kv+b)
        effic_esa_cs = self[2].good().start()['counts'].sum()/self[0].good().start()['counts'].sum()
        return(inc_flux*effic_esa_cs*ap_window*effic_tof_H(pac_kv))

