import numpy as np
import pandas as pd

# Find the tof file if it exists
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

def dat_loc(fil,home,dtype = ''):
    import os
    # f_indicator = fil.strip('.rec').split('_')[-2:]

    f_indicator = fil.split('.')[0].split('_')
    for f in getListOfFiles(home):
        if all(find.lower() in f.lower() for find in f_indicator) and '.rec' not in f and dtype in f:
            return(f)

def get_dat(s_run_loc,
             combine = True,
             dtype = '',
                  ref_nam = 'file_name',
                    load_dt = lambda x: np.nan,
                        load_params = {},home = './'):

#     dats = {}
#     for fil,ref_nam in zip(s_run_loc[fil_col].values,s_run_loc[ref_nam].values):
#         floc = dat_loc(str(fil).strip('.rec'),home = directory)
#         if floc:
#             dats[str(ref_nam)] = load_dt(floc,**load_params)
#     return(dats)
    dats = {}
    for rn in s_run_loc[ref_nam].keys():
        dats[str(rn)] = []
        
    for fil,rn in zip(s_run_loc[ref_nam].values,s_run_loc[ref_nam].keys()):
        floc = dat_loc(str(fil).strip('.rec'),home = home,dtype = dtype)
        if floc:
            dats[str(rn)].append(load_dt(floc,**load_params))
    if combine:
        for lab,vals in dats.items():
            if vals:
                dats[lab] = pd.concat(vals,ignore_index = True)
            else:pass
    return(dats)
    