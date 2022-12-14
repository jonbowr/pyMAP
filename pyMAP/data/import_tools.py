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
                    reduce = False):
    # Function to search directory and load in all data of a given type

    import os
    import pandas as pd
    fils = getListOfFiles(dirName)
    
    if reduce:
        dats = []
        for fil in fils:
            f = os.path.basename(fil).split('.')[0]
            if dtype in f:
                ds = load_dt(fil,dtype = dtype,**load_params)
                ds['name'] = f.replace(dtype,'')
                ds['file'] = fil
                ds['dtype'] = dtype
                dats.append(ds.set_index(['name','file','dtype']))
        return(pd.concat(dats))
    else:
        ds = {}
        ds['name'] = []
        ds[dtype+'_file'] = []
        ds[dtype] = []    
        
        for fil in fils:
            f = os.path.basename(fil).split('.')[0]
            if dtype in f:
                ds['name'].append(f.replace(dtype,'').lower())
                ds[dtype+'_file'].append(fil)
                ds[dtype].append(load_dt(fil,dtype = dtype,**load_params))
                
        return(pd.DataFrame(ds).set_index('name'))


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
        dat_parts.append(other.iloc[np.digitize(base_id,other_id)-1].reset_index())
    return(pd.concat(dat_parts,axis = 1))