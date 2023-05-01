# This is a function which takes the path of a .csv of the type XXXRAW_DE.csv
# and returns one array with data stacked and ready for cleaning using the cleaning 
# function. The only input required is the path relative to current directory.

def get_data_from_csv(rel_file_path):
    # Import the Numpy package to handle arrays.
    import numpy 
    print('1',rel_file_path)
    # Create empty arrays for all the relavant values (valid flags and tof values).
    # This is where the columns from the CSV will appeneded. We keep the valid flags
    # for cleaning
    
    tof0=numpy.empty((0))
    valstrt0=numpy.empty((0))
    valstp0=numpy.empty((0))
    valtof0=numpy.empty((0))
    
    tof1=numpy.empty((0))
    valstrt1=numpy.empty((0))
    valstp1=numpy.empty((0))
    valtof1=numpy.empty((0))
    
    tof2=numpy.empty((0))
    valstrt2=numpy.empty((0))
    valstp2=numpy.empty((0))
    valtof2=numpy.empty((0))
    
    
    tof3=numpy.empty((0))
    valstrt3=numpy.empty((0))
    valstp3=numpy.empty((0))
    valtof3=numpy.empty((0))
    
    # Read csv into a structured array using numpy. The "name=True" flag associates  
    # the columns with the name at the top of the csv file.
    dat=numpy.genfromtxt(rel_file_path, delimiter=',', names=True)
    
    
    # This for loop will cycle over all the names of the columns in the dat array
    # and appends the relevant values to the empty arrays created earlier. The for loop
    # will do a condition based search(if statments) using the first part of the 
    # column name. If the first part of the name is a match then the column is appended.
    for name in dat.dtype.names:
        #print(name[:11])  #print statment for debugging the string search.
        if name[:4]=='TOF0':
            tof0=numpy.append(dat[name],tof0)
        if name[:11]=='VALIDSTART0':
            valstrt0=numpy.append(dat[name],valstrt0)
        if name[:10]=='VALIDSTOP0':
            valstp0=numpy.append(dat[name],valstp0)
        if name[:9]=='VALIDTOF0':
            valtof0=numpy.append(dat[name],valtof0)
            
            
        if name[:4]=='TOF1':
            tof1=numpy.append(dat[name],tof1)
        if name[:11]=='VALIDSTART1':
            valstrt1=numpy.append(dat[name],valstrt1)
        if name[:10]=='VALIDSTOP1':
            valstp1=numpy.append(dat[name],valstp1)
        if name[:9]=='VALIDTOF1':
            valtof1=numpy.append(dat[name],valtof1)
            
            numpy.append
        if name[:4]=='TOF2':
            tof2=numpy.append(dat[name],tof2)
        if name[:11]=='VALIDSTART2':
            valstrt2=numpy.append(dat[name],valstrt2)
        if name[:10]=='VALIDSTOP2':
            valstp2=numpy.append(dat[name],valstp2)
        if name[:9]=='VALIDTOF2':
            valtof2=numpy.append(dat[name],valtof2)
            
            
        if name[:4]=='TOF3':
            tof3=numpy.append(dat[name],tof3)
        if name[:11]=='VALIDSTART3':
            valstrt3=numpy.append(dat[name],valstrt3)
        if name[:10]=='VALIDSTOP3':
            valstp3=numpy.append(dat[name],valstp3)
        if name[:9]=='VALIDTOF3':
            valtof3=numpy.append(dat[name],valtof3)
        
        
    # Turn individual arrays into one large array and return that array 
    dat_arr=numpy.empty((tof3.shape[0],17))
    dat_arr[:,0] = valstrt0.copy()
    dat_arr[:,1] = valstp0.copy()
    dat_arr[:,2] = valtof0.copy()
    dat_arr[:,3] = tof0.copy()
    dat_arr[:,4] = valstrt1.copy()
    dat_arr[:,5] = valstp1.copy()
    dat_arr[:,6] = valtof1.copy()
    dat_arr[:,7] = tof1.copy()
    dat_arr[:,8] = valstrt2.copy()
    dat_arr[:,9] = valstp2.copy()
    dat_arr[:,10] = valtof2.copy()
    dat_arr[:,11] = tof2.copy()
    dat_arr[:,12] = valstrt3.copy()
    dat_arr[:,13] = valstp3.copy()
    dat_arr[:,14] = valtof3.copy()
    dat_arr[:,15] = tof3.copy()
    
    # Compute the checksum and add it to the returned array. This will be used in cleaning 
    # function.
    dat_arr[:,16]=dat_arr[:,15]+dat_arr[:,3]-dat_arr[:,7]-dat_arr[:,11] #checksum

    return dat_arr
