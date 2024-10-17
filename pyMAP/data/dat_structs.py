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
        self.source = 'Sniffer'
        self.ref_nam = 'file_name'
        self.df = run.load(fasrun,'',page_names,instrument).drop_duplicates()
        self.df.reset_index(inplace = True)
        self.df.set_index('run_n',inplace = True)
        self.__df__ = self.df.copy()
        self.data_cols = []

    def import_dat(self,d_types = {'dat_sensor':['ILO_IFB','ILO_TOF_BD','ILO_RAW_CNT'],
                                    'dat_DE':['ILO_RAW_DE']
                                    },
                        dat_home = None,replace = False):

        if dat_home is None:
            dl = self.dhome
        else:
            dl = dat_home
        self.df = run.import_data(self.df,
                            dl,
                                d_types,
                                instrument = self.instrument,
                                ref_nam= self.ref_nam,source = self.source,replace = replace)
        
        for l in (d_types if type(d_types) is list else [d_types]):
            if l not in self.__df__:
                self.__df__[l] = self.df[l]
                self.data_cols.append(l)
            else:
                self.__df__[l].loc[self.df.index] = self.df[l]
        
        # elif type(d_types) is str:
        #     self.__df__[d_types].loc[self.df.index] = self.df[d_types]
            # self.data_cols.append(d_types)
        return(self)

    def load_dat(self,dat_fil = 'auto'):
        from pandas import read_pickle,DataFrame
        import numpy as np
        if dat_fil == 'auto':
            self.df = read_pickle(os.path.basename(self.doc).split('.')[0]+'.pkl')
        else:
            self.df = read_pickle(dat_fil)


        data_cols = list(self.df.keys()[self.df.apply(\
                        lambda x: np.any(x.apply(lambda xx: type(xx) is DataFrame)))])
        

        self.drop_empty(data_cols,how = 'all')

        # for l in self.df.keys():
        #     if l not in self.__df__.keys():
        #         self.__df__[l]= self.df[l]

        # if data_cols is None:
        #     data_cols = list(self.data_cols)
        for l in data_cols:
            if l not in self.__df__.keys():
                print(l)
                self.__df__[l] = self.df[l]
                self.data_cols.append(l)
            else:
                self.__df__[l].loc[self.df[l].index] = self.df[l]
        return(self)

    def save_dat(self,dat_fil = 'auto'):
        if dat_fil == 'auto':
            self.__df__.to_pickle(os.path.basename(self.doc).split('.')[0]+'.pkl')
        else:
            self.df = pd.read_pickle(dat_fil)        


    def __getitem__(self,item):
        return(self.df[item])

    def __setitem__(self,item,val):
        self.df[item] = val

    def refresh(self):
        self.df = self.__df__.copy()
        self.data_cols = []

    def mask(self,mask):
        self.df = self.df.loc[mask]

    def drop_empty(self,subset = None,how = 'any'):
        self.df = self.df.dropna(axis = 0,subset = subset,how = how)

