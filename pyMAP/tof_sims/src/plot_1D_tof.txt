######################### Plot 1D tof spectra from CSV#############    
# Function to produce plots using the remove_delayline_effects(), get_data_from_csv() function and clean_dat() 
# function. The function takes the relative path of the raw-de.csv file as the only required 
# input. The options are 
# tof = list of tofs we want to plot so, if we wanted a tof0 plot then tof=[0]. 
        #for tof0 and tof3 then tof=[0,3].
#chksm_flg = apply check sum when True
#clean = list of 4 binary values to check for valid flags( see clean_dat.py for more info
#plot_filename = a cutom name for the plots used for title and saving strings.
#axis = give figure access if figure is started before function is called. 
#xlim = the range of tofs to bin and plot.
#ylim = the rane of y plot.
#bins = number of bins in the range of xlim. 
#save = save a the figure as a .png file, should only be used when no figure is already 
        #started before function is called. 
#label = plot lable to use in ledgend if a figure started outside of the function and more 
        #than one plot will go the plotting axis

def plot_1D_tof(rel_file_path, tof=[0,1,2,3], chksm_flg = False, clean=[0,0,0,0], plot_filename='Unamed Run', \
                axis='None', xlim=[1,351], ylim=[1,10**5],bins=350, save=False, label='None'):
    
    # Import numpy and matplotlib's pyplot library to use for array handeling and plotting 
    # the 1-D tof spectra respectively.
    import matplotlib.pyplot
    import numpy
    
    # Call the get_data_from_csv(), clean_dat(), and remove_delayline_effects() to get data 
    #from csv, clean , and remove delayline effects. A .py file for each function has more 
    #indepth description of how eash is done.
    dat=get_data_from_csv(rel_file_path)
    dat=clean_dat(dat,valarr=clean,chksm_flg= chksm_flg)
    tof0,tof1,tof2,tof3,checksum=remove_delayline_effects(dat)
    
    
    # Stack the 1-D arrays from each tof to create a 2-D array. This is done for use in the 
    #for loop that handeles the tof=[] input. 
    dat=numpy.column_stack((tof0,tof1,tof2,tof3))
    
    
    # Create array to store binned data values used in the TOF histograms. This one of the 
    # values returned by this function( the other is the bins which are the same for all TOF 
    # histograms. 
    ct_arr=numpy.zeros((bins, len(tof)))
    
    # for loop to cycle over the tof=[] optional argument. The default is tof[0,1,2,3] and 
    # will produce plots in seperate figures for all 2 TOF spectra. 
    for tofi in tof:
        
        # check if an axis is provided to the function, and create a 1 axis figure, if no
        # none is provided. The title is also created here using the filename if none is 
        # provided by the plotfilename="" optional argument. If an axis is provided then we
        # use that axis for the plot and leave the title to be assigned from outside the 
        #function.
        if axis=='None':
            fig, ax = matplotlib.pyplot.subplots()
            ax.set_title(plot_filename)            
        else:
            ax = axis[tofi]
        print('ax=',ax)
        
        
        # Check if label is provided by the optional argument, label="" and sets it for the 
        # histogram. This is the lable matplotlib will use if a legend is created for the 
        # axis. If no label is provided the plot is made w/o a label for use in the legend.
        if label=='None':
            cnt,binsi,patch=ax.hist(dat[:,tofi],bins=bins,range=[xlim[0],xlim[1]])
        else:
            cnt,binsi,patch=ax.hist(dat[:,tofi],bins=bins,range=[xlim[0],xlim[1]], label=label)



        # Assign the counts from the histogram to the correct column in the counts array 
        # returned below 
        ct_arr[:,tofi]=cnt.copy()
        
        
        #Create plot and set options.
        ax.set_xlim(xlim[0],xlim[1])
        ax.set_ylim(ylim[0],ylim[1])
        ax.set_yscale('log')
        ax.set_title('TOF'+str(tofi))
        bin_wdth= (xlim[1]- xlim[0])/bins
        ax.set_ylabel('Counts per '+str(round(bin_wdth))+' nsec BIN')
        ax.grid(True)
        
        # Check if the save==True and save the figure. 
        if save==True:
            fig.savefig(plot_filename+'_TOF'+str(tofi)+'.png')
        
        
        # The binsi array just contains the left bin edges.
    return ct_arr, binsi