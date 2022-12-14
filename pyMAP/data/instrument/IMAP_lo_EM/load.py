import pandas as pd
import numpy as np

def load_DE_v1(loc):
    df = pd.read_csv(loc,header = 0)
    print('Loading %s'%loc)
    return(df.apply(lambda x: pd.to_numeric(x, errors = 'coerce')).dropna())

loadlib = {
            'TOF_DE_sample':{
                            'v001':load_DE_v1
                            },
            'ILO_RAW_DE':{
                            'v001':load_DE_v1
                            },
            'ILO_TOF_BD':{
                            'v001':load_DE_v1
                            },
            'ILO_IFB':{
                            'v001':load_DE_v1
                            },
            'ILO_RAW_CNT':{
                            'v001':load_DE_v1
                            }
            }

def load(as_runloc,dtype = 'TOF_DE_sample',version = 'v001'):
    return(loadlib[dtype][version](as_runloc))