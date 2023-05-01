####################Remove Delay Line Effects from TOF0 and TOF1#########################

# This function removes delay line effect from IMAP-Lo TOF0 and TOF1 spectra. The only input
# is the array produced by get_data_from_csv.py

def remove_delayline_effects(dat):
    #compute new TOF0 and TOF1 and create arrays from each TOF(0-3). The checksum is also 
    #returned and gets its own array.
    dat[:,3]=dat[:,3]-((12.5-dat[:,15])/2)
    dat[:,7]=dat[:,7]-((12.5+dat[:,15])/2)
    #tof2=dat[:,11].copy()
    #tof3=dat[:,15].copy()
    #checksum=dat[:,16].copy()
    
    return dat#tof0,tof1,tof2,tof3,checksum