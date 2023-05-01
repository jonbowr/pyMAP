###################Function to clean the data #####################

# This functions accepts input arrays in the format produced by the 
# get_data_from_csv() function. This function takes one required 
# argument which is the data array. The other options are

#valvalarr = a list with flag values for [tof0,tof1,tof2,tof3] each being either 1 or 0
#chksm_flg = Flag that sets the checksum threashfold when true . This should be used for golden triples only.
#chksm_cut = This is the threshold used when chksm_flg is True
def clean_dat(dat,valarr=[1,1,1,1],chksm_flg= True, chksm_cut=1):
    # Import numpy to handle arrays.
    import numpy
    
    if valarr[0] is not int:
        valarr=[int(i) for i in valarr]
    print('Checksum',chksm_cut)
    print('valid flags', valarr, valarr[0], valarr[0] is int )
    # Check the chksm_flg list and clean the data array. This is done with 
    # conditions applied one flag at a time. When a chksm_flg element is set to 1 
    # start, stop and tof need to be 1 for the event to make the cut.
    if valarr[0]==1:
        dat=dat[dat[:,0]==1,:]
        dat=dat[dat[:,1]==1,:]
        dat=dat[dat[:,2]==1,:]
    if valarr[1]==1:
        dat=dat[dat[:,4]==1,:]
        dat=dat[dat[:,5]==1,:]
        dat=dat[dat[:,6]==1,:]
    if valarr[2]==1:
        dat=dat[dat[:,8]==1,:]
        dat=dat[dat[:,9]==1,:]
        dat=dat[dat[:,10]==1,:]
    if valarr[3]==1:
        dat=dat[dat[:,12]==1,:]
        dat=dat[dat[:,13]==1,:]
        dat=dat[dat[:,14]==1,:]
        
    # Apply checksum threashold.
    if chksm_flg==True:
        dat=dat[numpy.absolute(dat[:,16])<chksm_cut, :]

        
    return dat