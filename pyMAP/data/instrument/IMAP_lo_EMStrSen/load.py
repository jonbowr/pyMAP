import pandas as pd
import numpy as np

def fix_angle(df):
    # loc = abs(df['azm'])==999
    time = df.reset_index()['time']
    df['scan_dir'] = df['azm']/abs(df['azm'])
    ang = (time-np.mean(time))*df['azm']/abs(df['azm'])
    df['phi'] = ang
    return(df)

def load_strSen_v1(loc):
    head = ['time','v_pmt','azm','v_str']
    df = pd.read_csv(loc,header = None,delimiter='\t',names = head)
    return(fix_angle(df))

loadlib = {
            'strSen':{
                            'v001':load_strSen_v1
                            },
            }

def load(as_runloc,dtype = 'strSen',version = 'v001'):
    
    df = loadlib[dtype][version](as_runloc)

    return(df)

