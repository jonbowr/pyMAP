import numpy as np
import pandas as pd
from pyMAP.data.load import getListOfFiles,dat_loc
# Find the tof file if it exists




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
                dats[str(rn)].append(load_dt(ff,dtype = dtype,**load_params))

    for lab,vals in dats.items():
        if vals:
            dats[lab] = pd.concat(vals,ignore_index = True)
        else: 
            dats[lab] = np.nan
    return(dats)

