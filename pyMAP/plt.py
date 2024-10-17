import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#plot the time of flights of the files
from scipy.ndimage import gaussian_filter as gf

def tofs_1d(dats,hist_plt = ['TOF0','TOF1','TOF2','TOF3'],
                        bins = 75,
                        bin_range = {
                                'TOF0': [10,350],
                               'TOF1':[10,250],
                               'TOF2':[10,150],
                               'TOF3':[.1,20]},  
                        logbins = False,
                        norm = None,
                        legend = False,
                        legend_loc='inside',
                        tof_ref_lines = {},
                        units ='[nS]',
                        title = ''):

    from pyMAP import bowPy as bp

    # parse bin input type to define the dict of bin arrays
    hist_bins = {}
    if type(bins) is int:
        for pl in hist_plt:
            if logbins and pl!= 'TOF3':
                hist_bins[pl] = np.geomspace(*bin_range[pl],bins)
            else:
                hist_bins[pl] = np.linspace(*bin_range[pl],bins)
    elif type(bins) is list: 
        for pl,bi in zip(hist_plt,bins):
            if logbins and pl!= 'TOF3':
                hist_bins[pl] = np.geomspace(*bin_range[pl],bi)
            else:
                hist_bins[pl] = np.linspace(*bin_range[pl],bi)
    else: hist_bins = {n:bins for n in hist_plt}
    
    # Define subplots structure
    if len(hist_plt)>1:
        fig,axs = plt.subplots(np.ceil(len(hist_plt)/1).astype(int),1,sharey = False)
    else:
        fig,ax = plt.subplots()
        axs = np.array([ax])
    fig.set_size_inches(9,4*len(axs))

    # Setup itter
    if type(dats) is dict or type(dats) is pd.Series:
        itter = dats.items()
    elif type(dats) is pd.DataFrame:
        itter = zip([''],[dats])
    else: 
        itter = dats

    # Itterate over data input type to allow for easy overplotting of spectra
    for lab,thing in itter:
        slabel = str(lab)
        labs = {}
        for nam,ax in zip(hist_plt,axs.reshape(-1,1).flatten()):
            cent = np.nanmean(thing[nam])
            h,bino = np.histogram(thing[nam],bins = hist_bins[nam])[:2]

            logbin_check =(logbins and nam != 'TOF3') 
            if logbin_check:
                h = h/(bino[1:]-bino[:-1])
                ax.semilogx()
            mid = (bino[:-1]+bino[1:])/2

            if norm == 'max':
                ax.plot(mid,h/np.nanmax(h),alpha = .4,
                    label = slabel,)
            else:
                ax.hist(thing[nam],bins = hist_bins[nam],density = logbin_check ,alpha = .2,
                    label = slabel,histtype = 'stepfilled')
                ax.hist(thing[nam],bins = hist_bins[nam],density = logbin_check,alpha = .8,
                        histtype = 'step',color = 'k')
    
    for nam,ax in zip(hist_plt,axs.reshape(-1,1).flatten()):
        ax.set_xlabel(' '.join([nam,units]))
        ax.set_xlim(min(hist_bins[nam]),max(hist_bins[nam]))
        ax.set_ylabel('counts')
        if tof_ref_lines !={}:
            from .tof import tof_expected,tof3_peaks_ns
            ref_tofs = tof_expected(**tof_ref_lines)
            if nam != 'TOF3':
                if len(ref_tofs['ke'].unique())>1:
                    ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[nam],'%.0f, %.0f'%(x['ke'],x['m']),ax = ax),axis = 1)
                    bp.plotJon.annot.vline(ax.get_xlim()[0],'[eV,amu]',ax = ax)
                else:
                    ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[nam],'%.0f'%(x['m']),ax = ax),axis = 1)
                    bp.plotJon.annot.vline(ax.get_xlim()[0],'[amu]',ax = ax)
            # else:
            #     for tof,lab in zip(tof3_peaks_EM,tof3_lables):
            #         bp.plotJon.annot.vline(tof,lab,ax = ax)
            #     bp.plotJon.annot.vline(ax.get_xlim()[0],'loEM',ax = ax)
        if legend and legend_loc.lower() == 'inside':
            ax.legend()
    axs[0].set_title(title)
    if legend and legend_loc.lower()=='outside':
        from pyMAP.bowPy.bowPy.plotJon.legend import legend_loc as ll
        ll(fig = fig,ax = axs[0])
    else:
        fig.tight_layout()
    return(fig,axs)

def tofs_2d(thing,pltx,plty,bins = 75,
                        bin_range = {
                                'TOF0':[.1,350],
                               'TOF1':[.1,250],
                               'TOF2':[.1,150],
                               'TOF3':[.1,50]},
                        plt_type = 'scatter',
                        fig = None,
                        ax = None,
                        logbins = False,
                        logcol =True,
                        units ='[nS]',
                        tof_ref_lines = {},
                        tof_mass_line = None):
    # Function to plot 2d histogram plot data. Bins pltx and plty columns from thing
    #   thing [pd.DataFrame]: containing columns pltx and pltx for plotting
    #   pltx,plty [str]: keys of tof dimension to plot along the x/y axis
    # plt_type [str]: keyword of plot to generate ['scatter','hist2d']

    from pyMAP import bowPy as bp
    # Define the histogram bins
    hist_bins = {}
    if type(bins) is int:
        for pl in [pltx,plty]:
            print(bin_range[pl])
            if logbins:
                hist_bins[pl] = np.geomspace(*bin_range[pl],bins)
            else:
                hist_bins[pl] = np.linspace(*bin_range[pl],bins)
    elif type(bins) is list: 
        for pl,bi in zip([pltx,plty],binnum):
            print(bin_range[pl])
            if logbins:
                hist_bins[pl] = np.geomspace(*bin_range[pl],bi)
            else:
                hist_bins[pl] = np.linspace(*bin_range[pl],bi)
    else:hist_bins = bins

    # Generate plot if none provided
    if ax is None:
        fig,ax = plt.subplots()
        fig.set_size_inches(8,6)
    
    # Plot the data
    if plt_type == 'hist2d':
        x = (hist_bins[pltx][1:]+hist_bins[pltx][:-1])/2
        y = (hist_bins[plty][1:]+hist_bins[plty][:-1])/2
        cnts = np.histogram2d(thing[pltx],thing[plty],
                              bins = [hist_bins[pltx],hist_bins[plty]],density = True)[0].T
        ax.pcolormesh(x,y,(np.log(cnts)if logcol else cnts))
    elif plt_type == 'scatter':
        bp.plotJon.plt.density_scatter(thing[pltx],thing[plty],
                               ax = ax,
                               bins = [hist_bins[pltx],hist_bins[plty]],
                               log_color = logcol,
                               alpha = .5,marker = '.')

    # Format the plot
    ax.set_xlabel(' '.join([pltx,units]))
    ax.set_ylabel(' '.join([plty,units]))
    if logbins:
        ax.loglog()

    xrng = ax.get_xlim()
    yrng = ax.get_ylim()
    if tof_ref_lines !={}:
        from .tof import tof_expected
        ref_tofs = tof_expected(**tof_ref_lines)
        if len(ref_tofs['ke'].unique())>1:
            ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[pltx],'%.0f, %.0f'%(x['ke'],x['m']),ax = ax),axis = 1)
            ref_tofs.apply(lambda x: ax.axhline(x[plty]),axis = 1)
            bp.plotJon.annot.vline(ax.get_xlim()[0],'[eV,amu]',ax = ax)
        else:
            ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[pltx],'%.0f'%(x['m']),ax = ax),axis = 1)
            ref_tofs.apply(lambda x: ax.axhline(x[plty]),axis = 1)
            bp.plotJon.annot.vline(ax.get_xlim()[0],'[amu]',ax = ax)

    if tof_mass_line !=None:
        from .tof import mass_line
        mline = mass_line(tof_mass_line)
        ax.plot(mline[pltx],mline[plty],label = 'mass line')
    ax.set_xlim(xrng)
    ax.set_ylim(yrng)

    return(fig,ax)

def tofs_comprehensive(dats,
                        bins = 75,
                        bin_range = {
                                'TOF0': [.1,350],
                               'TOF1':[.1,250],
                               'TOF2':[.1,150],
                               'TOF3':[.1,50]},  
                        logbins = False,
                        tof_ref_lines = {},
                        tof_mass_line = None,
                        units ='[nS]',
                        logy = False,
                        title = ''
                        ):
    fig,axs = tofs_1d(dats,bins = bins,
                           bin_range = bin_range,
                           tof_ref_lines = tof_ref_lines,
                           logbins= logbins)
    axs[0].set_title(title)
    if logy:
        for ax in axs:
            ax.semilogy()

    tofx = ['TOF0','TOF2','TOF0']
    tofy = ['TOF1','TOF1','TOF2']
    for xpl,ypl in zip(tofx,tofy):
        fig,ax = tofs_2d(dats,xpl,ypl,
                bins = bins,
                bin_range = bin_range,
                tof_ref_lines = tof_ref_lines,
                logbins= logbins,
                tof_mass_line = tof_mass_line,plt_type = 'hist2d')
        ax.set_title(title)
        fig.set_size_inches(8,6)
        fig.tight_layout()

# define dict with same keys as data_groups to setup plot groups of data
#   might want to move this to a different locaiton or combine somehow with data_groups
standard_groups = {
        'ILO_EM_status':
            {
            'single_rates [cts/s]':['START_A', 'START_C', 'STOP_B0', 'STOP_B3'],                 
            'tof_rate[cts/s]':['TOF0','TOF1','TOF2','TOF3','SILVER'],             
            'Efficiency':['Eff_A','Eff_B','Eff_C','Eff_TRIP'],      
           'Monitors':['MCP_VM','MCP_CM','MCP_VSET','PAC_VSET','PAC_VM','PAC_CM'],          
           # 'volts[V]':['TOF_MCP_VM','PAC_VM_volt'],  
           'Board Temp':['TEMP1','TEMP0','LV_TEMP','MCP_TEMP','PAC_TEMP'],        
           'Threshold register':['AN_A_THR_REG','AN_B0_THR_REG','AN_B3_THR_REG','AN_C_THR_REG'],                    
           } ,
        'ILO_INST_Status':
            {
                 'Currnent Monitor [mA]': ['MCP_CM','TOF_MCP_CM'],
             'MCP volts [V]': ['MCP_VM','TOF_MCP_VM', ],
                'MCP Monitors':['MCP_VSET_MON','MCP_OCP_MON'],
             'PAC volts [V]': [ 'PAC_VM','PAC_VSET',],
                'Monitors':['PAC_VSET_MON','HV_DIS_HK_N','PAC_OCP_MON'],
             'Board Temp': ['TEMP1', 'TEMP0', 'LV_TEMP', 'MCP_TEMP', 'PAC_TEMP'],
              'instrument status bits':['PAC_ENB[0]','PAC_ENB[1]','PAC_ENB_1','MCP_ENB[0]',
                                        'MCP_ENB[1]','MCP_ENB_1','PAC_ENB_2','MCP_ENB_2'],
             'LV [v]':['V12P0_VM','V12N0_VM'],                  
           } ,
       'EM_status_comp':
        {
             'Currnent Monitor [mA]': ['MCP_CM','TOF_MCP_CM'],
             'MCP volts [V]': ['MCP_VM','TOF_MCP_VM', ],
                'MCP Monitors':['MCP_VSET_MON','MCP_OCP_MON'],
             'PAC volts [V]': [ 'PAC_VM','PAC_VSET',],
                'Monitors':['PAC_VSET_MON','HV_DIS_HK_N','PAC_OCP_MON'],
             'Board Temp': ['TEMP1', 'TEMP0', 'LV_TEMP', 'MCP_TEMP', 'PAC_TEMP'],
              'instrument status bits':['PAC_ENB[0]','PAC_ENB[1]','PAC_ENB_1','MCP_ENB[0]',
                                        'MCP_ENB[1]','MCP_ENB_1','PAC_ENB_2','MCP_ENB_2'],
             'LV [v]':['V12P0_VM','V12N0_VM'],
            'single_rates [cts/s]':['START_A', 'START_C', 'STOP_B0', 'STOP_B3'],                 
            'tof_rate[cts/s]':['TOF0','TOF1','TOF2','TOF3','SILVER'],
            },
        'ILO_EM_rates':
            {
            'single_rates [cts/s]':['START_A', 'START_C', 'STOP_B0', 'STOP_B3','TOF3'],                 
            'tof_rate[cts/s]':['TOF0','TOF1','TOF2','SILVER'],             
            'Efficiency':['Eff_A','Eff_B','Eff_C','Eff_TRIP']
            },
        'ILO_FM_rates':
            {
            'single_rates [cts/s]':['rSTART_A', 'rSTART_C', 'rSTOP_B0', 'rSTOP_B3','rTOF3'],                 
            'tof_rate[cts/s]':['rTOF0','rTOF1','rTOF2','rSILVER'],             
            'Efficiency':['Eff_A','Eff_B','Eff_C','Eff_TRIP']
            } 
        }

def df_plot_groups(df,plt_grps={},fmt = '',plt_input = {},
                                fig = None,axs = None,
                                legend = True,err = False,df_err = None):
    # plots columns of datframe df defined by selector plt_groups 
    if type(plt_grps) == str:
        plt_grps = standard_groups[plt_grps]

    if axs is None:
        fig,axs = plt.subplots(len(plt_grps.keys()),sharex = True)
    fig.set_size_inches(10,len(axs)*4)
    for lab,vals,ax in zip(plt_grps.keys(),plt_grps.values(),axs):
        for y in plt_grps[lab]:
            if err:
                ax.errorbar(df.index,df[y],df[y],fmt=fmt,label = y,**plt_input)
            else:
                ax.plot(df[y],fmt,label = y,**plt_input)
        ax.set_ylabel(lab)
        if legend:ax.legend()
    axs[-1].set_xlabel(df.index.name)
    return(fig,axs)
    