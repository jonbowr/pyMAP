import pandas as pd
import numpy as np
from .EM_data_types import EM_dtypes

import pyMAP.pyMAP.tools.time as time_set

def load_DE_v1(loc):
    df = pd.read_csv(loc,header = 0)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0)
    df['SHCOARSE'] = time_set.spin_to_shcoarse(df['SPIN_SECONDS'].values)
    return(df.set_index('SHCOARSE'))

def load_HK_v1(loc):
    df = pd.read_csv(loc,header = 0)
    len1 = len(df)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0).drop_duplicates(subset = 'SHCOARSE').set_index('SHCOARSE')
    len2 = len(df)
    if (len1-len2)/len1>.1:
        from warnings import warn
        warn('Data corruption:Large Ammount of Dropped Measurements')
    return(df.drop_duplicates())

def load_IFB_v1(loc):
    df = pd.read_csv(loc,header = 0)
    len1 = len(df)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0)
    df = df.astype(dtype = EM_dtypes['ILO_IFB']).drop_duplicates(subset = 'SHCOARSE').set_index('SHCOARSE')
    len2 = len(df)
    if (len1-len2)/len1>.1:
        from warnings import warn
        warn('Data corruption:Large Ammount of Dropped Measurements')
    df['PAC_VM_volt'] = df['PAC_VM']*7500 #Use Brians voltage calculation to transform mon value to volts
    return(df)

def load_CNT_v1(loc):
    # cnt rate and tof files both have TOF0 keys, may want to rename the rates
    from pyMAP.pyMAP.tof import get_eff
    df = pd.read_csv(loc,header = 0)

    len1 = len(df)
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna(axis = 0).drop_duplicates(subset = 'SHCOARSE').set_index('SHCOARSE')
    
    len2 = len(df)
    if (len1-len2)/len1>.1:
        from warnings import warn
        warn('Data corruption:Large Ammount of Dropped Measurements')
    return(get_eff(df))

def load_RAW_DE_v1(loc):
    # check the headder for names and assign datatypes
    nanvals = {
            'TOF0':0.4225755257233885,
            'TOF1':0.458300954435785,
            'TOF2':0.3144102748020856,
            'TOF3':1.1962577109060106   
            }

    def nan_col_vals(keys):
        nan_cols = {}
        for lab in keys:
            lab = lab.strip()
            if 'tof' in lab.lower() and 'valid' not in lab.lower():
                nan_cols[lab] =nanvals[lab.split('_')[0]]
        return(nan_cols) 
    
    def raw_DE_type_getter(lab):
        if 'valid' in lab.lower():
            return('integer')
        elif 'tof' in lab.lower() or 'offset_ms' in lab.lower() or 'spin' in lab.lower():
            return('float')
        else:
            return('float')
    
    fil = open(loc,'r')
    head = fil.readline().split(',')
    fil.close()
    #import data from csv, assign blank tofvalues to nans
    df = pd.read_csv(loc,header = 0,
                     na_values = nan_col_vals(head),
                     # na_filter = False,
                     low_memory=False,
                     )
    # remove empty data rows
    df = df.iloc[(pd.to_numeric(df['DIRECT_EVENT_COUNT'],errors = 'coerce')>0).values]
    # Assign Index
    df.set_index(['SPIN_SECONDS','SPIN_SUBSECONDS', 'DIRECT_EVENT_COUNT'],append = True,inplace = True)
    
    # Stack counts put in standard DE format
    nk = df.keys().to_frame()[0].str.split('_').apply(lambda x: pd.Series([ '_'.join(x[:-1]),x[-1]]))
    nk.columns = ['TOF','order']
    df.columns = pd.MultiIndex.from_frame(nk)
    df = df.stack().reset_index()

    #Drop empty trailing data
    df = df.iloc[pd.to_numeric(df['order'],errors = 'coerce').values<
                    pd.to_numeric(df['DIRECT_EVENT_COUNT'],errors = 'coerce').values]
    #Drop data without any valid tofs
    df = df.iloc[np.logical_or.reduce(df[['VALIDTOF%d'%i for i in range(4)]].values.T)]

    # Define dataframe as numeric and assign data types to the columns
    dtypes = {l.strip():raw_DE_type_getter(l.strip()) for l in df.keys()}
    df = df.apply(lambda x: pd.to_numeric(x, errors = 'coerce',downcast = dtypes[x.name])).dropna(axis = 0,how = 'all')
    
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

def load(as_runloc,dtype = 'TOF_DE_sample',version = 'v001',timeZone = 'est'):
    
    print('Loading %s'%as_runloc)
    df = loadlib[dtype][version](as_runloc)

    # attempt to assign datetime index if index fails, resort to default SHCOARSE
    try:
        df['dateTime'] = df.index.to_series().apply(time_set.shcoarse_to_datetime)
        try:
            df['dateTime'] = df['dateTime'].apply(time_set.localize_to_tz,zone = timeZone)
        except:
            import warnings
            warnings.warn('Time Stamp Localization Failed')
        
    except: 
        import warnings
        from datetime import datetime as dt
        warnings.warn('Time Indexing Failed, Use SHCOARSE instead')
        df['dateTime'] = time_set.localize_to_tz(dt(2010, 1, 1, 0, 0, 0))

    return(df.reset_index().set_index('dateTime'))