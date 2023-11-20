import pandas as pd
import numpy as np
from . import asrun
from pyMAP.pyMAP.data.load import load as loader

def load_v1(f_as_run,home = './',sheet_name = 0):
    import os
    df = pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                sheet_name = sheet_name,
                header=2,
                index_col = [0,1,2,3]
                ),axis = 1).T.reset_index(level =0, drop = True ).T
    df = df.dropna(axis = 0,how = 'all')
    df = df.dropna(axis = 1,how = 'all')
    return(df)

def ETU_v1(f_as_run,home = './',sheet_name = 0):
    import os
    df = pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                sheet_name = sheet_name,
                header=5,
                ),axis = 1).T.reset_index(level =0, drop = True ).T
    df = df.dropna(axis = 0,subset = ['activity','file_name'])
    df = df.dropna(axis = 1,how = 'all')
    return(df.set_index(['date','run_n','activity']))

loadlib = {'v001':load_v1,
            'ibex_lo_etu':ETU_v1}
pages = {
        'v001':['Global',
                'M145_beam',
                'M145_system',
                'ETU_sensor',
                'ETU_tof'],
        'v002':['Global',
                'M145_beam',
                'M145_system',
                'EM_optics',
                'EM_tof',
                'Princeton_PSPL']
        }

def load(as_runloc,home = './',page_names = pages['v002'],version = 'v001'):
    return(loadlib[version](as_runloc,home,sheet_name = page_names))