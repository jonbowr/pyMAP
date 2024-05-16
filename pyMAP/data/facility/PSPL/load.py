import pandas as pd
import numpy as np

def load_abm_v1(loc):
    
    df = pd.read_csv(loc,usecols = range(6))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['effic'] = df['COIN Rate']**2/(df['OUT CEM Rate']*df['IN CEM Rate'])
    df['abs_mean'] =df['COIN Rate']/df['effic'] 
    return(df.set_index('Start Time'))

loadlib = {
            'ABM-Counts':load_abm_v1
            }

def load(as_runloc,dtype = 'strSen',version = 'v001'):
    print(as_runloc)
    # try:
    df = loadlib[dtype](as_runloc)
    return(df)
    # except:return(np.nan)
