from . import instrument,asrun
import numpy as np
import pandas as pd
loadlib = {
            'imap_lo_em':instrument.IMAP_lo_EM.load,
            'ibex_lo_etu':instrument.IBEX_lo_ETU.load,
            'EMstrSen':instrument.IMAP_lo_EMStrSen.load
            # 'asrun':asrun.load
            }

def load(loc,
            dtype = 'TOF_DE_sample',
            instrument = 'imap_lo_em',
                        load_params = {}):
    import os
    if os.path.isfile(loc):
        return(loadlib[instrument](loc,dtype,**load_params))
    elif os.path.isdir(loc):
        return(get_all_dat(loc,dtype,loadlib[instrument],**load_params))
    else:
        return(loadlib[instrument](dat_loc(os.path.basename(loc),
                                           os.path.dirname(loc),dtype = dtype)[0],dtype,**load_params))

def getListOfFiles(dirName):
    import os
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def get_all_dat(dirName = './',
                    dtype = '',
                    load_dt = lambda x: np.nan,
                    load_params = {},
                    reduce = False,
                    run_tag = ''):
    # Function to search directory and load in all data of a given type
    import os
    import pandas as pd
    fils = getListOfFiles(dirName)
    
    if reduce:
        dats = []
        for fil in fils:
            f = os.path.basename(fil)#.split('.')[0]
            if dtype in f:
                try:
                    ds = load_dt(fil,dtype = dtype,**load_params)
                    # ds['name'] = f.replace(dtype,'')
                    ds['fRAW'] = f
                    # ds[dtype+'_fil'] = f
                    dats.append(ds)
                except: 
                    import warnings
                    warnings.warn('LOAD FAILED ON FILE: %s'%fil)
        return(pd.concat(dats,axis = 0).sort_index())
    else:
        ds = {}
        ds['name'] = []
        ds[dtype+'_file'] = []
        ds[dtype] = []    
        
        for fil in fils:
            f = os.path.basename(fil)#.split('.')[0]
            if dtype in f and run_tag in f:
                # try:
                    nam = f.replace(dtype,'').lower()
                    # ds['name'].append('_'.join(nam.split('_')[:-2]))
                    df = load_dt(fil,dtype = dtype,**load_params)
                    df['fRAW'] = f
                    ds[dtype].append(df)
                    # add name as a tag, remove last 4 characters to give files with same tag,
                    # generated within same 100s the same name
                    ds['name'].append(nam)
                    ds[dtype+'_file'].append(fil)
                # except: 
                #     print('LOAD FAILED ON FILE: %s'%f)
        dats = pd.DataFrame(ds)
        dats.groupby('name').agg({dtype+'_file':list,
                                 dtype:lambda x: pd.concat(list(x),axis = 0).sort_index()})
        return(dats.set_index('name'))

def get_all_dfils(dirName = './',
                    dtype = '',
                    load_dt = lambda x: np.nan,
                    load_params = {},
                    run_tag = ''):
    # Function to search directory and find all data files of a given type and grab some metadata
    import os
    import pandas as pd
    import pyMAP.pyMAP.tools.time as time_set
    fils = getListOfFiles(dirName)
    
    ds = {}
    ds['name'] = []
    ds['file_path'] = []
    ds['file_size'] = []
    ds['dtype'] = []
    ds['created'] = []
    ds['last_modified'] = [] 

    for fil in fils:
        f = os.path.basename(fil)#.split('.')[0]
        if dtype in f and run_tag in f:
            # try:
                nam = f.replace(dtype,'').lower()
                # add name as a tag, remove last 4 characters to give files with same tag,
                # generated within same 100s the same name
                ds['name'].append(f)
                ds['file_path'].append(fil)
                ds['file_size'].append(os.path.getsize(fil)*10**-6)
                ds['dtype'].append(dtype)
                file_times = time_set.get_file_times(fil)
                ds['created'].append(file_times[0])
                ds['last_modified'].append(file_times[1])

            # except: 
            #     print('LOAD FAILED ON FILE: %s'%f)
    dats = pd.DataFrame(ds)
    dats.groupby('name').agg({'file_path':list})
    return(dats.set_index('name'))


def combiner(base,other_in, usecol = 'index'):
    # use np.in1d to combine values between data frames
    def rng_norm(arr):
        return((arr-min(arr))/(max(arr)-min(arr)))
    
    if type(other_in) != list:
        other_IT = [other_in]
    else: 
        other_IT = other_in
        
    dat_parts = [base.reset_index()]
    for other in other_IT: 
        if usecol == 'index':
            base_id = base.index
            other_id = other.index
        elif usecol == 'index_norm':
            base_id = rng_norm(base.index)
            other_id = rng_norm(other.index)
        else: 
            base = base.sort_values(usecol)
            other = other.sort_values(usecol)
            base_id = base[usecol]
            other_id = other[usecol]
        dat_parts.append(other.iloc[np.digitize(base_id,other_id)-1].reset_index().drop(
                                                    columns = (other_id.name if usecol == 'index' else usecol)))
    return(pd.concat(dat_parts,axis = 1))

def dat_loc(file_name,home,dtype = ''):
    # Function to locate a file path from a file name
    # File names considered to be unique ignoring case and underscores
    import os

    # make input filename itterable if just a string
    if type(file_name) == str:
        file_name = [file_name]
    if type(file_name)==list:
        file_name = pd.Series(file_name)

    thing = pd.DataFrame(getListOfFiles(home),columns = ['loc'])
    thing['nam'] = thing['loc'].apply(lambda x: os.path.basename(x).split('.')[0].replace('_','').lower())
    thing['type'] = thing['loc'].apply(lambda x: os.path.splitext(x)[1])
    thing = thing.loc[~thing['type'].str.lower().str.contains('rec')]
    indic = file_name.apply(lambda x: x.split('.')[0].replace('_','').lower())

    return(indic.apply(lambda x: thing.loc[\
                    np.logical_and(thing['nam'].str.contains(x),
                        thing['nam'].str.contains(dtype))]['loc'].values[0]))

    # fs = []
    # for f in getListOfFiles(home):
    #     for fil in file_name:
    #         f_indicator = fil.split('.')[0].replace('_','').lower()
    #         ff = os.path.basename(f).split('.')[0].replace('_','').lower()
    #         if f_indicator in ff and '.rec' not in f and dtype in f:
    #             fs.append(f)
    # return(fs)