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
                    reduce = True):
    import os
    import pandas as pd
    fils = getListOfFiles(dirName)
    # dats = []



    # for fil in fils:
    #     f = os.path.basename(fil).split('.')[0]
    #     if dtype in f:
    #         ds = load_dt(fil,**load_params)
    #         ds['name'] = f.replace(dtype,'')
    #         ds['file'] = fil
    #         ds['dtype'] = dtype
    #         dats.append(ds.set_index(['name','file','dtype']))

    # return(pd.concat(dats))

    ds = {}
    ds['name'] = []
    ds[dtype+'_file'] = []
    ds[dtype] = []
    
    
    for fil in fils:
        f = os.path.basename(fil).split('.')[0]
        if dtype in f:
            ds['name'].append(f.replace(dtype,'').lower())
            ds[dtype+'_file'].append(fil)
            ds[dtype].append(load_dt(fil,**load_params))
            
    return(pd.DataFrame(ds).set_index('name'))