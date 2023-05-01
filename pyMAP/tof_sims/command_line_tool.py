################ TOF Command Line Tool#######################################
# This is a command line tool that uses the functions get_data_from_csv(), clean_data(), remove_delay_line_effects(), 
# and several plotting functions to display IMAP-Lo calibration data. The goal is to make this easy to use to produce
# TOF plot with only the file name being required. The point is that anyone can run this with no more input than
# required to display spectra. The options are meant to be useful for people that have more complicated needs.



############################# Create Argument Parser ############################





def argParsing():

    parser = argparse.ArgumentParser(description='This tool accepts a GSEOS file path and makes cool plots of for IMAP-Lo.')
    
    
    parser.add_argument('-f', '--file',
                            help='the GSEOS RAW_DE_...#.csv event filepath',
                           dest='file', type=str,
                           required=True)
    
    parser.add_argument('-v', '--valid',
                        help='valid flags for TOF0, TOF1, TOF2, TOF3',
                        nargs="+", default=[0,0,0,0], 
                        dest='valid' )
    
    parser.add_argument('-ch', '--checksum',
                        help='Apply, absloute value of, checksum < 1 filter. To change from 1, provide a value after the flag',
                        nargs='?', default='None', const=True,
                        dest='chksm' )
                           
    parser.add_argument('-p', '--plot',
                        help='Which plots to produce? Default is both 1D and 2D. For 1D plot provide the tof0-3 value or list for 2D',
                        nargs='+', default='None', 
                        dest='plots' )
    
    parser.add_argument('-del', '--delayed',
                        help='Flag to not remove delay line effects from a plot. The effect is removed by default to avoid confusion.',
                        type=bool, default=False, 
                        dest='delayed')
    
    parser.add_argument('-x', '--xrange',
                        help='start, stop, number of bins values for x-axis in plots ',
                        nargs=3, default=[0.1,350.1, 350], type =float,
                        dest='xrange' )
    
    parser.add_argument('-y', '--yrange',
                        help='start, stop, number of bins values for y-axis in plots.',
                        nargs=3, default=[0.1,350.1, 350], type =float,
                        dest='yrange' )
    
    parser.add_argument('-o', '--output',
                        help='the plot output file name w/o extention. default is input file name with out.csv. ',
                        default = 'None',
                        dest='outFile')
                        
    parser.add_argument('-st', '--spttle',
                        help='Title to use for plots if different from -o or default ',
                        default = 'None',
                        dest='spttle')                    
                        
    
    
    
                        
    

    return parser.parse_args()






################################### Main Code #######################################
#####################################################################################
#####################################################################################

import argparse
import matplotlib.pyplot
import numpy
from src.get_data_from_csv import *
from src.clean_dat import *
from src.remove_delayline_effects import *
from src.plot_1D_tof import *
from src.plot_2d_data import *

#####################################################Parsing#################################################################################

# Parse commandline arguments.
args= argParsing()

####################################################Plotting################################################################################


#read data file into an array with columns of [valstrt_tof0,valstop_tof0,valtof0, tof0, valstrt_tof1,..., tof3,checksum ]
raw_de_array = get_data_from_csv(args.file)


#####################################################Cleaning##################################################################################

#check for cleaning option from the parser.
# Here is where we use  -v,-ch 
if args.chksm == 'None':
    chksm_fl_ps=False
    chksm_val_ps='NA'
    clean_data_array = clean_dat(raw_de_array,valarr=args.valid,chksm_flg= False)
elif args.chksm == True:
    chksm_fl_ps=True
    chksm_val_ps= 1
    clean_data_array = clean_dat(raw_de_array,valarr=args.valid,chksm_flg= True)
else:
    chksm_fl_ps=True
    chksm_val_ps=float(args.chksm)
    clean_data_array = clean_dat(raw_de_array,valarr=args.valid,chksm_flg= True, chksm_cut=float(args.chksm))
    
print('Data array shape before cleaning = ',raw_de_array.shape)
print('Valid flags used = ',args.valid)
print('Checksum flag = ',chksm_fl_ps)
print('Absloute value of checksum < ',chksm_val_ps)
print('Data array shape after cleaning = ', clean_data_array.shape) 
print(clean_data_array[0,:])
print(raw_de_array[0,:])


# Delay line effects are removed by default to avoid confuion during testing. If the -del flag is supplied to 
# parser then delay line effects remain in the spectra, which is rarly desired. 
if args.delayed == True:
    pass
else:
    clean_data_array = remove_delayline_effects(clean_data_array)

    
    

#####################################################plotting#####################################################
#Create labels and output file names based on -o and -st options stored as args.outFile and args.spttle
# If none is given then use input file path to create some strings for use in plotting.
# The name creation 
if args.outFile == 'None':
    splitter = args.file[:-4].split('\\')
    if len(splitter) ==1:
        out_dir ='./'
    else:
        out_dir = args.file[:(-len(splitter[-1]))]
       
    if args.spttle =='None':
        spttle=splitter[-1]
        spttle_fsize=8
    out_fname = out_dir+spttle
else:
    splitter = args.outFile.split('\\')
    if len(splitter) ==1:
        out_dir ='./'
    else:
        out_dir = args.outFile[:(-len(splitter[-1]))]
       
    if args.spttle =='None':
        spttle=splitter[-1]
        spttle_fsize=12
    else:
        spttle=args.spttle
        spttle_fsize=12
    
    out_fname = args.outFile


# create xrange and yrange variables for ease of use in plotting functions.    
xrange=args.xrange
yrange=args.yrange



# save cleaned data array as csv
sav_arr=numpy.column_stack((clean_data_array[:,3].copy(), clean_data_array[:,7].copy(), clean_data_array[:,11].copy(), clean_data_array[:,15].copy(), clean_data_array[:,16].copy()))
numpy.savetxt(out_fname+'.csv', sav_arr, delimiter=',', header='TOF0, TOF1, TOF2, TOF3, CHECKSUM')



#Check plotting options provided by -p if the argument is not called then a default set of plots are produced.
# if -p is called but no argument is given then the program should exit and give invalid argument error.
# if -p is selected and only one number from 0-4 is given then only a 1D plot with 0-4 being tof0, tof1, tof2, tof3, checksum .
# if -p is selected and 2 integers are given, i,j(=0-4) and i!=j then 1 2D plot is produced with 1-D histograms on the edge.

if args.plots == 'None':
    fig, ax = matplotlib.pyplot.subplots(3,1,figsize=(5, 8), constrained_layout=True)
    
    im1 = plot_2d_data(clean_data_array, tofij=[0,2], xlims=xrange[:2],ylims=yrange[:2], runname='TOF0 vs TOF2', axis=ax[0], bins=[xrange[2],yrange[2]])
    ax[0].set_xlabel('TOF0[nsec]')
    ax[0].set_ylabel('TOF2[nsec]')
    fig.colorbar(im1[3], ax=ax[0])
    
    im2 = plot_2d_data(clean_data_array, tofij=[0,1], xlims=xrange[:2],ylims=yrange[:2], runname='TOF0 vs TOF1', axis=ax[1], bins=[xrange[2],yrange[2]])
    ax[1].set_xlabel('TOF0[nsec]')
    ax[1].set_ylabel('TOF1[nsec]')
    fig.colorbar(im2[3], ax=ax[1])
    
    im3 = plot_2d_data(clean_data_array, tofij=[1,2], xlims=xrange[:2],ylims=yrange[:2], runname='TOF1 vs TOF2', axis=ax[2], bins=[xrange[2],yrange[2]])
    ax[2].set_xlabel('TOF1[nsec]')
    ax[2].set_ylabel('TOF2[nsec]')
    fig.colorbar(im3[3], ax=ax[2])
    
    fig.suptitle(spttle, fontsize=spttle_fsize)
    fig.savefig(out_fname+'_2D.png', dpi=1200)
    fig.show()
    
    
    fig1, ax1 = matplotlib.pyplot.subplots(3,1,figsize=(5, 8), constrained_layout=True)
    
    
    ct_arr0, binsi0=plot_1D_tof(clean_data_array, tof=[0], plot_filename='TOF0', axis=ax1[0], xlim=xrange[:2],bins=xrange[2])
    ct_arr0, binsi0=plot_1D_tof(clean_data_array, tof=[1], plot_filename='TOF1', axis=ax1[1], xlim=xrange[:2],bins=xrange[2])
    ct_arr0, binsi0=plot_1D_tof(clean_data_array, tof=[2], plot_filename='TOF2', axis=ax1[2], xlim=xrange[:2],bins=xrange[2])
    fig1.suptitle(spttle, fontsize=spttle_fsize)
    fig1.savefig(out_fname+'_1D.png', dpi=1200)
    
    
    fig2, ax2 = matplotlib.pyplot.subplots(2,1,figsize=(4, 6), constrained_layout=True)
    ct_arr3, binsi3=plot_1D_tof(clean_data_array, tof=[3], plot_filename='TOF3', axis=ax2[0], xlim=[.01, 20.01],bins=80)
    ct_arr4, binsi4=plot_1D_tof(clean_data_array, tof=[4], plot_filename='Check Sum', axis=ax2[1], xlim=[-10,10],bins=80)
    ax2[1].set_xlabel('Checksum [nsec]')
    fig2.suptitle(spttle, fontsize=spttle_fsize)
    fig2.savefig(out_fname+'_1D_tof3Chksm.png', dpi=1200)
elif len(args.plots)==1:
    print("Oops, this can't be good! You found the end of the program. This means you are using options not included in the documentation. Stop it!")
elif len(args.plots)==2:
    print("Oops, this can't be good! You found the end of the program. This means you are using options not included in the documentation. Stop it!")
else:
    print("Oops, this can't be good! You found the end of the program. This means you are using options not included in the documentation. Stop it!")
