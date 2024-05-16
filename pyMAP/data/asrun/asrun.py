import numpy as np
import pandas as pd
from pyMAP.pyMAP.data.load import getListOfFiles,dat_loc
# Find the tof file if it exists
from pyMAP.pyMAP.data.load import load as loader




def get_dat(s_run_loc,
             dtype = '',
                    load_dt = lambda x: np.nan,
                        load_params = {},home = './'):
    dats = {}
    for rn in s_run_loc.keys():
        dats[str(rn)] = []
        
    if type(home) is str:
        hom = [home]*len(s_run_loc)
    else:
        hom = list(home)

    for fil,rn,hh in zip(s_run_loc.values,s_run_loc.keys(),hom):
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


def import_data(df,home,dtypes = ['ILO_TOF_BD','ILO_IFB','ILO_RAW_CNT','ILO_RAW_DE'],
                                                instrument = 'imap_lo_fm',interper = 'index',
                                            ref_nam = 'file_name',):
    if type(dtypes)==list:
        for tp in dtypes:
            df[tp] = get_dat(df[ref_nam],home = home,load_dt = loader,dtype = tp,load_params={'instrument':instrument}).values()
            df = df.dropna(axis = 0,subset = tp)
    elif type(dtypes) == dict:
        from pyMAP.pyMAP.tools.tools import concat_combine
        for lab,vals in dtypes.items():
            dats = pd.DataFrame([pd.Series(get_dat(df[ref_nam],home = home,load_dt = loader,
                                                   dtype = tp,load_params={'instrument':instrument})
                              ,name = tp) for tp in vals]).T
            def combiner(x):
                try:
                    return(concat_combine(list(x),interper))
                except:
                    print('Load Failed on file: %s'%str(x.name))
                    return(None)
                        
            df[lab] = dats.apply(combiner,axis = 1).values
    return(df)