import pandas as pd
import numpy as np

def load_EXAMPLE_v1(loc):
    df = pd.read_csv(loc,header = 0)
    return(df)


loadlib = {
            'EXAMPLE':{
                            'v001':load_EXAMPLE_v1
                            },
            }

def load(as_runloc,dtype = 'TOF_DE_sample',version = 'v001',timeZone = 'est'):
    
    df = loadlib[dtype][version](as_runloc)

    return(df)