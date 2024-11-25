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
        from numpy import nan
        self.doc = fasrun
        self.dhome = data_home
        self.pages = page_names
        self.instrument = instrument
        self.source = 'Sniffer'
        self.ref_nam = 'file_name'
        self.df = run.load(fasrun,'',page_names,instrument).drop_duplicates()
        self.df.reset_index(inplace = True)
        self.df.set_index('run_n',inplace = True)
        self.df = self.df.loc[~self.df.index.duplicated(keep='first')]
        self.df = self.df.replace('x',nan)
        self.__df__ = self.df.copy()
        self.data_cols = []

    def import_dat(self,d_types = {'dat_sensor':['ILO_IFB','ILO_TOF_BD','ILO_RAW_CNT'],
                                    'dat_DE':['ILO_RAW_DE']
                                    },
                        dat_home = None,replace = False,reduce_name = True):

        if dat_home is None:
            dl = self.dhome
        else:
            dl = dat_home
        self.df = run.import_data(self.df,
                            dl,
                                d_types,
                                instrument = self.instrument,
                                ref_nam= self.ref_nam,source = self.source,
                                replace = replace,reduce_name = reduce_name)
        
        if type(d_types) is list:
            itterator = d_types
        elif type(d_types) is dict:
            itterator = d_types.keys()
        else: 
            itterator = [d_types] 

        for l in itterator:
            if l not in self.__df__:
                self.__df__[l] = self.df[l]
                self.data_cols.append(l)
            else:
                self.__df__.loc[self.df.index,l] = self.df[l]
        
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
        for lab in self.df.keys():
            if lab not in self.__df__:
                data_cols.append(lab)

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
                self.__df__.loc[self.df[l].index,l] = self.df[l]
        return(self)

    def save_dat(self,dat_fil = 'auto'):
        if dat_fil == 'auto':
            self.__df__.to_pickle(os.path.basename(self.doc).split('.')[0]+'.pkl')
        else:
            self.df.to_pickle(dat_fil)        


    def __getitem__(self,item):
        return(self.df[item])

    def __setitem__(self,item,val):
        self.df[item] = val

    def refresh(self):
        self.df = self.__df__.copy()
        # self.data_cols = []

    def mask(self,mask):
        self.df = self.df.loc[mask]

    def drop_empty(self,subset = None,how = 'any'):
        self.df = self.df.dropna(axis = 0,subset = subset,how = how)

    def append(self,df,axis =1,inplace = True):
        for lab in df.keys():
            if lab in self.df:
                self.df.loc[df.index,lab] = df[lab]
            else: 
                self.df[lab] = df[lab]
            if inplace: 
                if lab in self.__df__:
                    self.__df__.loc[df.index,lab] = df[lab]
                else: 
                    self.__df__[lab] = df[lab]
        return(self.df)
