import pandas as pd
import numpy as np

def load_strSen_v1(loc):
    head = ['time','v_pmt','azm','v_str']
    df = pd.read_csv(loc,header = None,delimiter='\t',names = head)
    return(df)


loadlib = {
            'strSen':{
                            'v001':load_strSen_v1
                            },
            }

def load(as_runloc,dtype = 'strSen',version = 'v001'):
    
    df = loadlib[dtype][version](as_runloc)

    return(df)