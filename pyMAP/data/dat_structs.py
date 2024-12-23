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

        '''
        Structure to control importing and loading asrun table structured data. Upon initialization asRunr will input the given asrun data table and search the local directory for .pkl with the same name as fasrun/doc and import data cols to  the existing dataframe (__df__)

        __init__ Inputs: 
            fasrun (str): File location for asrun .xlsx table listing test runs
            data_home (str): Folder location to search when importing desired runs
            page_names (list):  xlsx page names to be imported, all pages of the asrun table are imported and concatenated
                Standard input from final cal: ['Global','TOF','FM_optics','Princeton_PSPL']
                - view fasrun defined above for available options
            instrument (str): instrument option to be used to define set of data load functions
                Options: pyMAP.data.loadlib 
                    dict{
                     'imap_lo_em': <function pyMAP.pyMAP.data.instrument.IMAP_lo_EM.load.load>,
                     'imap_lo_fm': <function pyMAP.pyMAP.data.instrument.IMAP_lo_FM.load.load>,
                     'ibex_lo_etu': <function pyMAP.pyMAP.data.instrument.IBEX_lo_ETU.load.load>,
                     'EMstrSen': <function pyMAP.pyMAP.data.instrument.IMAP_lo_EMStrSen.load.load>,
                     'pspl': <function pyMAP.pyMAP.data.facility.PSPL.load.load>
                        }
            ref_name (str):

        Parameters
        ----------
        doc: str, xlsx doc loaded (see inputs fasrun)
        dhome: str, folder location of input data used to search for data files while performing import, see input data_home
        pages: list, see input page_names
        instrument: str, load library to use when importing data see input instrument: pyMAP.data.loadlib
        source: str/list, tag to filter data against when importing
            Options: 
            - 'Sniffer'
            - 'Instrument'
            Combine data aq option with unit options 
            - 'EU': engineering units
            - 'DN': data number
            e.g.: ['Sniffer','DN'] to import sniffer data with defined DN
        ref_nam: str, column of data frame for run hash to search for when importing data
        df: pandas.DataFrame giving the filtered data structure
        __df__: pandas.DataFrame giving the unfiltered complete data structure
        data_cols: list, additional data columns generated from data load and import


        '''
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
        '''
        Inport the given data and incorperated the resulting data tables to the asRunr via pyMAP.data.asRun.import_data
        Inputs:
            d_types: str/list/dict, data types to import via load functions. available data types are dependent on the instrument load package, and can be found via pyMAP.data.loadlib
                Examples: 
                    - 'ILO_IFB'
                    - 'ILO_TOF_BD'
                    - 'ILO_RAW_CNT'
                - If the input d_types is a string, a single column of the given data type is loaded and appended to the asRunr.df
                - if teh input d_types is a list, each element of list is loaded and appended to asRunr.df
                - if the input is a dict, it must be of the form:
                    d_types = {'dat_sensor':['ILO_IFB','ILO_TOF_BD','ILO_RAW_CNT'],
                                    'dat_DE':['ILO_RAW_DE']}
                    where the resulting  columns ['dat_sensor','dat_DE'] will be generated and concatenated from th listed data sets via pyMAP.data.asRun.import_data
            dat_home: see asRunr.dhome
            replace: bool [True/False] 
                - True: import and replace all d_types data cols
                - False: import all empty elements, but skip data that has already beem imported
            reduce_name: str, see pyMAP.data.asRun.import_data
        '''
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
        '''
            load data from pandas.DataFrame pickle, asRunr.data_cols from the pickle are appended to the existing data frame, and will fill in empty data elements of existing data_cols. All elements from the asRunr.df that already exist remain unchanged
        '''

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
        '''
        Save asRunr.__df__ to pandas.DataFrame.to_pickle, if dat_fil == 'auto' then the resulting pickle is assigned the same name as th asRunr.doc
        '''
        if dat_fil == 'auto':
            self.__df__.to_pickle(os.path.basename(self.doc).split('.')[0]+'.pkl')
        else:
            self.df.to_pickle(dat_fil)        


    def __getitem__(self,item):
        return(self.df[item])

    def __setitem__(self,item,val):
        self.df[item] = val

    def refresh(self):
        '''
        Replace asRunr.df with asRunr.__df__, effectively removing all masks and selections. 
        '''
        self.df = self.__df__.copy()
        # self.data_cols = []

    def mask(self,mask):
        '''
        assign boolean mask to asRunr.df via asRunr.df.loc[mask]. does not impact asRunr.__df__. 
        '''

        self.df = self.df.loc[mask]

    def drop_empty(self,subset = None,how = 'any'):
        '''
        Drop empty columns (subset) from asRunr.df via pandas.DataFrame.dropna
        '''
        self.df = self.df.dropna(axis = 0,subset = subset,how = how)

    def append(self,df,axis =1,inplace = True):
        '''
            Adds columns of values 
            Inputs: 
                - df: pandas.DataFrame to add to existing asRunr.df
                - axis: currenently unused
                - inplace: bool [True/False]: if true, values from df are also appended to core __df__ parameter, otherwise they are just appended to asRunr.df parameter
        '''
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
