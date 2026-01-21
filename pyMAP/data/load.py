from . import instrument,asrun,facility
import numpy as np
import pandas as pd
loadlib = {
            'imap_lo_em':instrument.IMAP_lo_EM.load,
            'imap_lo_fm':instrument.IMAP_lo_FM.load,
            'ibex_lo_etu':instrument.IBEX_lo_ETU.load,
            'EMstrSen':instrument.IMAP_lo_EMStrSen.load,
            'pspl':facility.PSPL.load
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
            if dtype in f and run_tag in f:
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
                    ds['name'].append('_'.join(nam.split('_')[:-2]))
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
                    run_tag = '',
                    required_tag = None,
                    name_format = None):
    # Function to search directory and find all data files of a given type and grab some metadata
    # dtype and run_tag can be strings or lists (optional filters)
    # required_tag is a required filter if provided (string or list)
    # name_format is an optional regex pattern or callable to validate filename format
    #   Example regex: r"^Instrument_FM\d+_T\d{3}_R\d{3}_.*_\d{8}T\d{6}_[A-Z]{2}\.csv$"
    #   Example callable: lambda fname: fname.startswith("Instrument_") and fname.endswith(".csv")
    import os
    import pandas as pd
    import re
    import pyMAP.pyMAP.tools.time as time_set
    fils = getListOfFiles(dirName)
    
    # Convert dtype and run_tag to lists if they're strings
    if isinstance(dtype, str):
        dtype_list = [dtype] if dtype else ['']
    else:
        dtype_list = list(dtype)
    
    if isinstance(run_tag, str):
        run_tag_list = [run_tag] if run_tag else ['']
    else:
        run_tag_list = list(run_tag)
    
    # Convert required_tag to list if it's a string
    if required_tag is not None:
        if isinstance(required_tag, str):
            required_tag_list = [required_tag] if required_tag else []
        else:
            required_tag_list = list(required_tag)
    else:
        required_tag_list = None
    
    # Compile regex pattern if name_format is a string
    if name_format is not None:
        if isinstance(name_format, str):
            name_pattern = re.compile(name_format)
            format_checker = lambda fname: name_pattern.search(fname) is not None
        elif callable(name_format):
            format_checker = name_format
        else:
            raise ValueError("name_format must be a string (regex) or callable")
    else:
        format_checker = None
    
    ds = {}
    ds['name'] = []
    ds['file_path'] = []
    ds['file_size'] = []
    ds['dtype'] = []
    ds['run_tag'] = []
    ds['required_tag'] = []
    ds['created'] = []
    ds['last_modified'] = [] 
    

    for fil in fils:
        f = os.path.basename(fil)#.split('.')[0]
        f_lower = f.lower()  # Case-insensitive comparison
        
        # Check name format if provided
        if format_checker is not None:
            try:
                format_valid = format_checker(f)
            except Exception as e:
                format_valid = False
                print(f"Warning: Format check failed for '{f}': {e}")
            
            if not format_valid:
                continue  # Skip files that don't match format
        else:
            format_valid = True
        
        # Check required_tag first (all required tags must be present) - case insensitive
        if required_tag_list is not None:
            req_match = all(rt.lower() in f_lower for rt in required_tag_list if rt)
            if not req_match:
                continue  # Skip files that don't match all required tags
            matched_required = ', '.join([rt for rt in required_tag_list if rt.lower() in f_lower])
        else:
            matched_required = ''
        
        # Check if any dtype matches - case insensitive
        dtype_match = any(dt.lower() in f_lower for dt in dtype_list if dt)
        if not dtype_list[0]:  # If empty list or empty string
            dtype_match = True
            matched_dtype = ''
        else:
            matched_dtype = next((dt for dt in dtype_list if dt.lower() in f_lower), None)
        
        # Check if any run_tag matches - case insensitive
        run_tag_match = any(rt.lower() in f_lower for rt in run_tag_list if rt)
        if not run_tag_list[0]:  # If empty list or empty string
            run_tag_match = True
            matched_run_tag = ''
        else:
            matched_run_tag = next((rt for rt in run_tag_list if rt.lower() in f_lower), None)
        
        if dtype_match and run_tag_match:
                nam = f
                if matched_dtype:
                    nam = nam.replace(matched_dtype, '').lower()
                
                ds['name'].append(f)
                ds['file_path'].append(fil)
                ds['file_size'].append(os.path.getsize(fil)*10**-6)
                ds['dtype'].append(matched_dtype if matched_dtype else dtype_list[0])
                ds['run_tag'].append(matched_run_tag if matched_run_tag else run_tag_list[0])
                ds['required_tag'].append(matched_required)
                file_times = time_set.get_file_times(fil)
                ds['created'].append(file_times[0])
                ds['last_modified'].append(file_times[1])

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

def dat_loc(file_name,home,dtype = '',selector = '',reduce_name = True):
    # Function to locate a file path from a file name
    # File names considered to be unique ignoring case and underscores
    import os

    # make input filename itterable if just a string
    if type(file_name) == str:
        file_name = [file_name]
    if type(file_name)==list:
        file_name = pd.Series(file_name)

    # thing = pd.DataFrame(getListOfFiles(home),columns = ['loc'])
    # thing['nam'] = thing['loc'].apply(lambda x: os.path.basename(x).split('.')[0].replace('_','').lower())
    # thing['type'] = thing['loc'].apply(lambda x: os.path.splitext(x)[1])
    # thing = thing.loc[~thing['type'].str.lower().str.contains('rec')]
    # indic = file_name.apply(lambda x: x.split('.')[0].replace('_','').lower())

    # return(indic.apply(lambda x: thing.loc[\
    #                 np.logical_and(thing['nam'].str.contains(x),
    #                     thing['nam'].str.contains(dtype))]['loc'].values[0]))

    def nam_reducer(st):
        strip = ['.txt','.csv']
        str_remove = ['_','-','.']
        st_new = st.lower()
        for strp in strip:
            st_new = st_new.strip(strp)
        for rep in str_remove:
            st_new = st_new.replace(rep,'')
        return(st_new)

    fs = []
    for f in getListOfFiles(home):
        for fil in file_name:
            if reduce_name: 
                f_indicator = nam_reducer(fil)
                ff = nam_reducer(os.path.basename(f))
            else: 
                f_indicator = str(fil)
                ff = os.path.basename(f)
            if type(selector) is str:
                picker = selector in os.path.basename(f)
            elif type(selector) is list:
                picker = np.all([s in os.path.basename(f) for s in selector])
            if f_indicator in ff and '.rec' not in f and dtype in f and picker:
                fs.append(f)
    return(fs)