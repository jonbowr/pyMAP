import pandas as pd
import numpy as np

import pyMAP.pyMAP.tools.time as time_set

def load_DE_v1(loc):
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0)
    df['SHCOARSE'] = time_set.spin_to_shcoarse(df['SPIN_SECONDS'].values)
    return(df.set_index('SHCOARSE'))

def load_HK_v1(loc):
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0).set_index('SHCOARSE')
    return(df)

def load_IFB_v1(loc):
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0).set_index('SHCOARSE')
    df['PAC_VM_volt'] = df['PAC_VM']*7500 #Use Brians voltage calculation to transform mon value to volts
    return(df)

def load_CNT_v1(loc):
    # cnt rate and tof files both have TOF0 keys, may want to rename the rates
    from pyMAP.pyMAP.tof import calc_eff
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0).set_index('SHCOARSE')
    return(calc_eff(df))

def load_RAW_DE_v1(loc):
    #import data from csv, drop corrupt lines
    df = pd.read_csv(loc,header = 0).apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0)
    # Assign Index
    df.set_index(['SPIN_SECONDS','SPIN_SUBSECONDS', 'DIRECT_EVENT_COUNT'],append = True,inplace = True)
    # Stack counts put in standard DE format
    nk = df.keys().to_frame()[0].str.split('_').apply(lambda x: pd.Series([ '_'.join(x[:-1]),x[-1]]))
    nk.columns = ['TOF','cnt']
    df.columns = pd.MultiIndex.from_frame(nk)
    df = df.stack().reset_index()
    # Calculate SHCOARSE from SPIN_SECONDS and assign as index
    df['SHCOARSE'] = time_set.spin_to_shcoarse(df['SPIN_SECONDS'].values)
    df.set_index('SHCOARSE',inplace = True)
    return(df)


loadlib = {
            'TOF_DE_sample':{
                            'v001':load_DE_v1
                            },
            'ILO_RAW_DE':{
                            'v001':load_RAW_DE_v1
                            },
            'ILO_TOF_BD':{
                            'v001':load_HK_v1
                            },
            'ILO_IFB':{
                            'v001':load_IFB_v1
                            },
            'ILO_RAW_CNT':{
                            'v001':load_CNT_v1
                            }
            }

def load(as_runloc,dtype = 'TOF_DE_sample',version = 'v001'):
    
    print('Loading %s'%as_runloc)
    df = loadlib[dtype][version](as_runloc)

    # attempt to assign datetime index if index fails, resort to default SHCOARSE
    try:
        df['time'] = df.index.to_series().apply(time_set.shcoarse_to_datetime)
        return(df.reset_index().set_index('time'))
    except: 
        import warnings
        warnings.warn('Time Indexing Failed, Default Index Used Instead')
        return(df)