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
    def __init__(self,
                    fasrun = '',
                    data_home = './',
                    page_names = [],
                    instrument = '',
                    ref_nam = 'file_name'):
        self.doc = fasrun
        self.dhome = data_home
        self.pages = page_names
        self.instrument = instrument
        self.ref_nam = 'file_name'
        self.df = run.load(fasrun,'',page_names,instrument)
        self.df.reset_index(inplace = True)
        self.df.set_index('run_n',inplace = True)
        self.__df__ = self.df.copy()
        self.data_cols = []

    def load_dat(self,d_types = {'dat_sensor':['ILO_IFB','ILO_TOF_BD','ILO_RAW_CNT'],
                                    'dat_DE':['ILO_RAW_DE']
                                    },
                        ):
        self.df = run.import_data(self.df,
                            self.dhome,
                                d_types,
                                instrument = self.instrument)

    def __getitem__(self,item):
        return(self.df[item])

    def __setitem__(self,item,val):
        self.df[item] = val

    def refresh(self):
        self.df = self.__df__.copy()
        self.data_cols = []

    def mask(self,mask):
        self.df = self.df.loc[mask]



