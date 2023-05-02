####################### 2D Plot of  RAW-DE.csv data ##############################
# This is a function that takes a RAW-DE.csv file and produces a 2D-hitogram/heatmap.
# The only required input is a relative path to the data file from the current directory.
# The optional arguments are 
# tofij = a list of 2 TOFs used for plotting. Default is tofij=[0,2] and produces a TOF0
        # vs. TOF1.
# xlims, ylims = limits to plot in tofi and tofj. default is 350 to cover entire TOF range 
        # in both tofi and tofj.
# runname= string to use for title if no axis given for plot.
# axis = axis to plot 2D image if figure was created outside the function. If no axis is 
        # given then a figure is created for plotting. 



def plot_2d_data(rel_file_path, tofij=[0,2], xlims=[.1,350],ylims=[.1,350], runname='Unamed Run', axis='None', bins=350):
    
    # Import numpy and matplotlib's pyplot library to use for array handeling and plotting 
    # the 1-D tof spectra respectively.
    import matplotlib.pyplot
    import numpy
    
    # Call the get_data_from_csv(), clean_dat(), and remove_delayline_effects() to get data 
    #from csv, clean , and remove delayline effects. A .py file for each function has more 
    #indepth description of how eash is done.
    dat=get_data_from_csv(rel_file_path)
    dat=clean_dat(dat,valarr=clean,chksm_flg= chksm_flg)
    tof0,tof1,tof2,tof3,checksum = remove_delayline_effects(dat)
    
    
    # Check if caller asked for tofi vs tofj but i=j and raise exception if true.
    if tofij[0]==tofij[1]:
        raise Exception("Sorry, you must choose different values. The options are 0-4 (TOF0,TOF1,TOF2,TOF3,Check Sum)")
    
    
    
    # Create labels for use in plots based on tofij=[i,j] option. if none is provided then
    #tof0 vs tof2 is shown.
    if tofij[0]== 0:
        tofi=tof0.copy()
        xlbl='TOF0'
    elif tofij[0]==  1:
        tofi=tof1.copy()
        xlbl='TOF1'
    elif tofij[0]== 2:
        tofi=tof2.copy()
        xlbl='TOF2'
    elif tofij[0]== 3:
        tofi=tof3.copy()
        xlbl='TOF3'
    elif tofij[0]== 4:
        tofi=checksum.copy()
        xlbl='Check Sum'
    else:
        raise Exception("Sorry, the options are 0-4 (TOF0,TOF1,TOF2,TOF3,Check Sum)")
        
        
        
    if tofij[1]== 0:
        tofj=tof0.copy()
        ylbl='TOF0'
    elif tofij[1]== 1:
        tofj=tof1.copy()
        ylbl='TOF1'
    elif tofij[1]== 2:
        tofj=tof2.copy()
        ylbl='TOF2'
    elif tofij[1]== 3:
        tofj=tof3.copy()
        ylbl='TOF3'
    elif tofij[1]== 4:
        tofj=checksum.copy()
        ylbl='Check Sum'
    else:
        raise Exception("Sorry, the options are 0-4 (TOF0,TOF1,TOF2,TOF3,Check Sum)")
    
    
    # Check if runname is provided and use to make string for title. If no name is given a 
    # generic title, in the form TOFi vs. TOFj, is used.
    if runname=='Unamed Run':
        runname=xlbl+' vs. '+ylbl
    else:
        runname = runname+' '+xlbl+' vs. '+ylbl
    
    # Check if an axis is given for the plot and create a figure if none is given.
    # If none is given then the labels and title created above will be used and a colorbar
    # flag raised. 
    if axis=='None':
        fig, ax = matplotlib.pyplot.subplots()
        ax.set_title(runname)
        ax.set_xlabel(xlbl+' (nsec)')
        ax.set_ylabel(ylbl+' (nsec)')
        colorb='yes'
    else:
        ax = axis
        colorb='no'
    # Plot 2D historam.
    im=ax.hist2d(tofi,tofj,bins=bins, norm=matplotlib.colors.LogNorm())
    ax.set_xlim(xlims[0],xlims[1])
    ax.set_ylim(ylims[0],ylims[1])
    ax.grid(True)
    
    # Check if a color bar flag was raied during the handeling of the axis argument.
    # If the flag was raised then create a colorbar from the hist2d object "im"
    if colorb=='yes':
        fig.colorbar(im[3], ax=ax)

    # Return the plot object to use for colorbar if figure is outside 
    # the function. The binned data is also returned (see matplotlib.pyplot.hist2d documentation online).
    return im