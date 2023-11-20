# import numpy as np
# from scipy.optimize import curve_fit as cf
# from scipy.interpolate import interp1d
# from .numJon.numJon import gauss_filt_nan as gf
# from .fitJon import funcs as fc

# class loTOF_DE:

#     def __init__(df,tof_bins = ):
#         ```
#         parameters: 
#             df: standard DE dataframe
#             df_status: instrument staus dataframe spanning timeframe
#             TOF Range:
#             TOF Bins:
#             info: Dataframe with columns showing, rows given for each data file input
#             - date
#             - instrument, 
#             - test, 
#             - test run, 
#             - pac voltage
#             - MCP voltage
#             - Threshold settings
#             - DE bit settings 
#             - KE beam
#             - Beam Species
#             filt:
#             - delay_removed:T/F
#             - Triples:T/F
#             - Checksum:np.inf
#             - speed: T/F
#             - Quadrant:
#             - tof_range:  
#         ```
import os
from . import asrun as run


class asRunr:
    def __init__(self,asrun_nam = '',
                 asrun_home = './',
                    asrun_pages = [],
                    instrument = '',
                    ref_nam = 'file_name'):
        self.doc = asrun_nam
        self.home = asrun_home
        self.pages = asrun_pages
        self.instrument = instrument
        self.ref_nam = 'file_name'
        self.df = run.load(asrun_nam,asrun_home,asrun_pages,instrument)
        self.__df__ = self.df.copy()
        self.data_cols = []

    def load_dat(self,dtype = '',drop_empty = False):
        from . import load,dat_loc
        self.df['%sloc'%dtype] = dat_loc(self.df[self.ref_nam],self.home,dtype)
        if '%sdat'%dtype not in self.data_cols:
            self.data_cols.append('%sdat'%dtype)
        self.df['%sdat'%dtype] = self.df['%sloc'%dtype].apply(load,dtype = dtype,instrument = self.instrument)
        # self.df['%sdat'%dtype] = run.get_dat(self.df,dtype,self.ref_nam,self.instrument)
        if drop_empty:
            self.mask(~self.df['%sdat'%dtype].apply(lambda x:x.empty))

    def __getitem__(self,item):
        return(self.df[item])

    def __setitem__(self,item,val):
        self.df[item] = val

    def refresh(self):
        self.df = self.__df__.copy()
        self.data_cols = []

    def mask(self,mask):
        self.df = self.df.loc[mask]
