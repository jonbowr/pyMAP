import pandas as pd
import numpy as np

def load_DE_v1(loc):
    df = pd.read_csv(loc,header = 0)
    return(df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna().set_index('SPIN_SECONDS'))

def load_HK_v1(loc):
    df = pd.read_csv(loc,header = 0)
    return(df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna().set_index('SHCOARSE'))

def load_CNT_v1(loc):
    # cnt rate and tof files both have TOF0 keys, may want to rename the rates
    from pyMAP.pyMAP.tof import calc_eff
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna().set_index('SHCOARSE')
    return(calc_eff(df))

loadlib = {
            'TOF_DE_sample':{
                            'v001':load_DE_v1
                            },
            'ILO_RAW_DE':{
                            'v001':load_DE_v1
                            },
            'ILO_TOF_BD':{
                            'v001':load_HK_v1
                            },
            'ILO_IFB':{
                            'v001':load_HK_v1
                            },
            'ILO_RAW_CNT':{
                            'v001':load_CNT_v1
                            }
            }

def load(as_runloc,dtype = 'TOF_DE_sample',version = 'v001'):
    print('Loading %s'%as_runloc)
    return(loadlib[dtype][version](as_runloc))