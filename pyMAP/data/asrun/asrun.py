import numpy as np
import pandas as pd
from pyMAP.pyMAP.data.load import getListOfFiles,dat_loc
# Find the tof file if it exists
from pyMAP.pyMAP.data.load import load as loader




def get_dat(s_run_loc,
             dtype = '',
                    load_dt = lambda x: np.nan,
                        load_params = {},home = './',source = '',
                        reduce_name = True):
    dats = {}
    for rn in s_run_loc.keys():
        dats[str(rn)] = []
        
    if type(home) is str:
        hom = [home]*len(s_run_loc)
    else:
        hom = list(home)

    for fil,rn,hh in zip(s_run_loc.values,s_run_loc.keys(),hom):
        floc = dat_loc(str(fil).strip('.rec'),home = hh,dtype = dtype,
                                selector = source,reduce_name = reduce_name)
        if floc:
            for ff in floc:
                try:
                        dats[str(rn)].append(load_dt(ff,dtype = dtype,**load_params))
                except:
                    print('Load Failed on file: %s'%str(rn))
    for lab,vals in dats.items():
        if vals:
            dats[lab] = pd.concat(vals,axis = 0,sort=True)
            # print(len(vals))
        else: 
            dats[lab] = np.nan

    return(pd.Series(dats))


def import_data(df,home,dtypes = ['ILO_TOF_BD','ILO_IFB','ILO_RAW_CNT','ILO_RAW_DE'],
                                                instrument = 'imap_lo_fm',interper = 'index',
                                            ref_nam = 'file_name',source = '',replace =False,
                                            reduce_name = True):

    def load_or(df,tp):
        if tp not in df.keys() or replace:
                df[tp] = get_dat(df[ref_nam],home = home,load_dt = loader,dtype = tp,
                                 load_params={'instrument':instrument},source = source,
                                 reduce_name = reduce_name)
        else:
            df.loc[df[tp].isna(),tp] = get_dat(df.loc[df[tp].isna()][ref_nam],home = home,load_dt = loader,dtype = tp,
                             load_params={'instrument':instrument},source = source,reduce_name = reduce_name)
        return(df)

    if type(dtypes)==list:
        for tp in dtypes:
            df =load_or(df,tp)
    elif type(dtypes)==str:
        for tp in [dtypes]:
            df =load_or(df,tp)
    elif type(dtypes) == dict:
        from pyMAP.pyMAP.tools.tools import concat_combine
        for lab,vals in dtypes.items():
            dats = pd.DataFrame([pd.Series(get_dat(df[ref_nam],home = home,load_dt = loader,
                                                   dtype = tp,load_params={'instrument':instrument},
                                                   source = source,reduce_name = reduce_name)
                              ,name = tp) for tp in vals]).T
            def combiner(x):
                try:
                    return(concat_combine(list(x),interper))
                except:
                    print('Load Failed on file: %s'%str(x.name))
                    return(None)
                        
            df[lab] = dats.apply(combiner,axis = 1).values
    return(df)