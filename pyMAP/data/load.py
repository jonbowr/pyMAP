from . import instrument,facility
import numpy as np
import pandas as pd
loadlib = {
            'imap_lo_em':instrument.IMAP_lo_EM.load
            }

def load(loc,instrument = 'imap_lo_em',
                            dtype = 'TOF_DE_sample',
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
            f = os.path.basename(fil).split('.')[0]
            if dtype in f:
                try:
                    ds = load_dt(fil,dtype = dtype,**load_params)
                    # ds['name'] = f.replace(dtype,'')
                    # ds['file'] = fil
                    ds[dtype+'_fil'] = fil
                    dats.append(ds)
                except: 
                    print('LOAD FAILED ON FILE: %s'%fil)
        return(pd.concat(dats,axis = 0).sort_index())
    else:
        ds = {}
        ds['name'] = []
        ds[dtype+'_file'] = []
        ds[dtype] = []    
        
        for fil in fils:
            f = os.path.basename(fil).split('.')[0]
            if dtype in f and run_tag in f:
                # try:
                    nam = f.replace(dtype,'').lower()

                    # ds['name'].append('_'.join(nam.split('_')[:-2]))

                    ds[dtype].append(load_dt(fil,dtype = dtype,**load_params))
                    ds['name'].append(nam[:-4])
                    ds[dtype+'_file'].append(fil)
                # except: 
                #     print('LOAD FAILED ON FILE: %s'%f)
        dats = pd.DataFrame(ds)
        dats.groupby('name').agg({dtype+'_file':list,
                                 dtype:lambda x: pd.concat(list(x),axis = 0).sort_index()})
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
        if usecol is 'index':
            base_id = base.index
            other_id = other.index
        elif usecol is 'index_norm':
            base_id = rng_norm(base.index)
            other_id = rng_norm(other.index)
        else: 
            base_id = base[usecol]
            other_id = other[usecol]
        dat_parts.append(other.iloc[np.digitize(base_id,other_id)-1].reset_index().drop(
                                                    columns = (other_id.name if usecol is 'index' else usecol)))
    return(pd.concat(dat_parts,axis = 1))

def dat_loc(file_name,home,dtype = ''):
    # Function to locate a file path from a file name
    # File names considered to be unique ignoring case and underscores
    import os

    # make input filename itterable if just a string
    if type(file_name) is str:
        file_name = [file_name]

    fs = []
    for f in getListOfFiles(home):
        for fil in file_name:
            f_indicator = fil.split('.')[0].replace('_','').lower()
            ff = os.path.basename(f).split('.')[0].replace('_','').lower()
            if f_indicator in ff and '.rec' not in f and dtype in f:
                fs.append(f)
    return(fs)