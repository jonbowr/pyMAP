import numpy as np
import pandas as pd
from pyMAP.pyMAP.data.import_tools import getListOfFiles
# Find the tof file if it exists


def dat_loc(fil,home,dtype = ''):
    import os
    # f_indicator = fil.strip('.rec').split('_')[-2:]

    f_indicator = fil.split('.')[0].replace('_','').lower()
    fs = []
    for f in getListOfFiles(home):
        ff = f.split('\\',)[-1].split('.')[0].replace('_','').lower()
        if f_indicator in ff and '.rec' not in f and dtype in f:
            fs.append(f)
    return(fs)

def get_dat(s_run_loc,
             dtype = '',
                  ref_nam = 'file_name',
                    load_dt = lambda x: np.nan,
                        load_params = {},home = './'):
    dats = {}
    for rn in s_run_loc[ref_nam].keys():
        dats[str(rn)] = []
        
    for fil,rn in zip(s_run_loc[ref_nam].values,s_run_loc[ref_nam].keys()):
        floc = dat_loc(str(fil).strip('.rec'),home = home,dtype = dtype)
        if floc:
            for ff in floc:
                dats[str(rn)].append(load_dt(ff,**load_params))

    for lab,vals in dats.items():
        if vals:
            dats[lab] = pd.concat(vals,ignore_index = True)
        else: 
            dats[lab] = np.nan
    return(dats)
    