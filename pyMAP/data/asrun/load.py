import pandas as pd
import numpy as np
from . import asrun

def load_v1(as_runloc,sheet_name = 0):
    df = pd.concat(pd.read_excel(as_runloc,
                sheet_name = sheet_name,header=2,index_col = np.arange(4))).stack().unstack(level  = [0,-1])
    df = df.dropna(axis = 0,how = 'all')
    df = df.dropna(axis = 1,how = 'all')
    df['data','dat_de'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = pd.read_csv,dtype = 'TOF_DE_sample').values()
    df['data','dat_tof'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = pd.read_csv,dtype = 'ILO_TOF_BD').values()
    df['data','dat_ifb'] = asrun.get_dat(df['ETU_tof'],home = '../Test Data/csv',load_dt = pd.read_csv,dtype = 'ILO_IFB').values()
    
    return(df.T.reset_index(level =0, drop = True ).T)

loadlib = {'v001':load_v1}
pages = {
        'v001':['Global',
                'M145_beam',
                'M145_system',
                'ETU_sensor',
                'ETU_tof']
        }

def load(as_runloc,version = 'v001'):
    return(loadlib[version](as_runloc,sheet_name = pages[version]))