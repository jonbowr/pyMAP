import numpy as np
import pandas as pd
from pyMAP.pyMAP.data.load import getListOfFiles,dat_loc
# Find the tof file if it exists
from pyMAP.pyMAP.data.load import load as loader



def get_dat(s_run_loc,
             dtype = '',
                  ref_nam = 'file_name',
                    load_dt = lambda x: np.nan,
                        load_params = {},home = './'):
    dats = {}
    for rn in s_run_loc[ref_nam].keys():
        dats[str(rn)] = []
        
    if type(home) is str:
        hom = [home]*len(s_run_loc)
    else:
        hom = list(home)

    for fil,rn,hh in zip(s_run_loc[ref_nam].values,s_run_loc[ref_nam].keys(),hom):
        floc = dat_loc(str(fil).strip('.rec'),home = hh,dtype = dtype)
        if floc:
            for ff in floc:
                dats[str(rn)].append(load_dt(ff,dtype = dtype,**load_params))

    for lab,vals in dats.items():
        if vals:
            dats[lab] = pd.concat(vals,axis = 0,sort=True)
        else: 
            dats[lab] = np.nan
    print(len(dats))
    return(dats)


def import_em_data(df,dloc):
    df['dat_de'] = get_dat(df,home = dloc,load_dt = loader,dtype = 'ILO_RAW_DE').values()
    df['dat_tof'] = get_dat(df,home = dloc,load_dt = loader,dtype = 'ILO_TOF_BD').values()
    df['dat_ifb'] = get_dat(df,home = dloc,load_dt = loader,dtype = 'ILO_IFB').values()
    # df['dat_de'] = get_dat(df,home = dloc,load_dt = loader,dtype = 'TOF_DE_sample').values()
    
    return(df)