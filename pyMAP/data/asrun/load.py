import pandas as pd
import numpy as np
from . import asrun
from pyMAP.pyMAP.data.load import load as loader

def load_v1(f_as_run,home = './',sheet_name = 0):
    import os
    
    # df = asrun.run_df(pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                # sheet_name = sheet_name,header=2,index_col = np.arange(4))).stack().unstack(level  = [0,-1]))
    # df['data','dat_de'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = loader,dtype = 'TOF_DE_sample').values()
    # df['data','dat_tof'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = pd.read_csv,dtype = 'ILO_TOF_BD').values()
    # df['data','dat_ifb'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = pd.read_csv,dtype = 'ILO_IFB').values()
    # return(df)


    df = pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                sheet_name = sheet_name,header=2,index_col = np.arange(4))).stack().unstack(level  = [0,-1]).T.reset_index(level =0, drop = True ).T
    df = df.dropna(axis = 0,how = 'all')
    df = df.dropna(axis = 1,how = 'all')
    dloc= os.path.join(home,'Test Data/csv')
    df['dat_de'] = asrun.get_dat(df,home = dloc,load_dt = loader,dtype = 'TOF_DE_sample').values()
    df['dat_tof'] = asrun.get_dat(df,home = dloc,load_dt = loader,dtype = 'ILO_TOF_BD').values()
    df['dat_ifb'] = asrun.get_dat(df,home = dloc,load_dt = loader,dtype = 'ILO_IFB').values()
    
    return(df)

loadlib = {'v001':load_v1}
pages = {
        'v001':['Global',
                'M145_beam',
                'M145_system',
                'ETU_sensor',
                'ETU_tof']
        }

def load(as_runloc,home = './',page_names = pages['v001'],version = 'v001'):
    return(loadlib[version](as_runloc,home,sheet_name = page_names))