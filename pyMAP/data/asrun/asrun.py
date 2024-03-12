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
            # print(len(vals))
        else: 
            dats[lab] = np.nan

    return(dats)


def import_em_data(df,home,dtypes = ['ILO_TOF_BD','ILO_IFB','ILO_RAW_CNT','ILO_RAW_DE'],combine = False):
    
    for tp in dtypes:
        df[tp] = get_dat(df,home = home,load_dt = loader,dtype = tp).values()
        df = df.dropna(axis = 0,subset = tp)
    if combine:
        from pyMAP.pyMAP.tools.tools import concat_combine
        df['EM_data'] =df.apply(lambda x: concat_combine([x[l].set_index('SHCOARSE') for l in dtypes],'index'),axis = 1) 
        for l in dtypes:
            df.drop(l,inplace = True)
    
    return(df)