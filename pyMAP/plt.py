import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

#plot the time of flights of the files
from scipy.ndimage import gaussian_filter as gf

def tofs_1d(dats,hist_plt = ['TOF0','TOF1','TOF2','TOF3'],
                        binnum = 75,
                        bin_range = {
                                'TOF0': [.1,350],
                               'TOF1':[.1,250],
                               'TOF2':[.1,150],
                               'TOF3':[.1,50]},  
                        logbins = False,
                        hist_bins = {},
                        norm = None,
                        legend = False,
                        legend_loc='inside',
                        tof_ref_lines = {},
                        units ='[nS]'
                        ):
    
    # legend_loc: str ['inside','right']

    from pyMAP import bowPy as bp

    # define the dict of bin arrays
    if hist_bins == {}:
        bins = {}
        if type(binnum) is int:
            for pl in hist_plt:
                print(bin_range[pl])
                if logbins and pl!= 'TOF3':
                    bins[pl] = np.geomspace(*bin_range[pl],binnum)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],binnum)
        elif type(binnum) is list: 
            for pl,bi in zip(hist_plt,binnum):
                print(bin_range[pl])
                if logbins and pl!= 'TOF3':
                    bins[pl] = np.geomspace(*bin_range[pl],bi)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],bi)
    else: bins = hist_bins
    
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

    for lab,thing in itter:

        slabel = str(lab)

        labs = {}

        for nam,ax in zip(hist_plt,axs.reshape(-1,1).flatten()):
            cent = np.nanmean(thing[nam])
            h,bino = np.histogram(thing[nam],bins = bins[nam])[:2]

            logbin_check =(logbins and nam != 'TOF3') 
            if logbin_check:
                h = h/(bino[1:]-bino[:-1])
                ax.semilogx()
            mid = (bino[:-1]+bino[1:])/2

            if norm == 'max':
                ax.plot(mid,h/np.nanmax(h),alpha = .4,
                    label = slabel,)
            else:
                ax.hist(thing[nam],bins = bins[nam],density = logbin_check ,alpha = .2,
                    label = slabel,histtype = 'stepfilled')
                ax.hist(thing[nam],bins = bins[nam],density = logbin_check,alpha = .8,
                        histtype = 'step',color = 'k')
    
    if tof_ref_lines !={}:
        from .tof import tof_expected
        ref_tofs = tof_expected(**tof_ref_lines)
    else: ref_tofs = []

    for nam,ax in zip(hist_plt,axs.reshape(-1,1).flatten()):
        ax.set_xlabel(' '.join([nam,units]))
        ax.set_xlim(min(bins[nam]),max(bins[nam]))
        ax.set_ylabel('counts')
        if tof_ref_lines !={} and nam != 'TOF3':
            ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[nam],'%.2d, %d'%(x['ke'],x['m']),ax = ax),axis = 1)
            bp.plotJon.annot.vline(ax.get_xlim()[0],'[eV,amu]',ax = ax)
        if legend and legend_loc.lower() == 'inside':
            ax.legend()

    fig.tight_layout()

    return(fig,axs)

def tofs_2d(thing,pltx,plty,binnum = 75,
                        bin_range = {
                                'TOF0':[.1,350],
                               'TOF1':[.1,250],
                               'TOF2':[.1,150],
                               'TOF3':[.1,50]},  
                        hist_bins = {}, 
                        fig = None,
                        ax = None,
                        logbins = False,
                        logcol =True,
                        units ='[nS]',
                        tof_ref_lines = {},
                        tof_mass_line = None):
    from pyMAP import bowPy as bp
    if hist_bins == {}:
        bins = {}
        if type(binnum) is int:
            for pl in [pltx,plty]:
                print(bin_range[pl])
                if logbins:
                    bins[pl] = np.geomspace(*bin_range[pl],binnum)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],binnum)
        elif type(binnum) is list: 
            for pl,bi in zip([pltx,plty],binnum):
                print(bin_range[pl])
                if logbins:
                    bins[pl] = np.geomspace(*bin_range[pl],bi)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],bi)
    else: bins = hist_bins
    if ax is None:
        fig,ax = plt.subplots()
        fig.set_size_inches(8,6)
    
    x = (bins[pltx][1:]+bins[pltx][:-1])/2
    y = (bins[plty][1:]+bins[plty][:-1])/2
    cnts = np.histogram2d(thing[pltx],thing[plty],
                          bins = [bins[pltx],bins[plty]],density = True)[0].T
    ax.pcolormesh(x,y,(np.log(cnts)if logcol else cnts))
    ax.set_xlabel(' '.join([pltx,units]))
    ax.set_ylabel(' '.join([plty,units]))
    if logbins:
        ax.loglog()

    if tof_ref_lines !={}:
        from .tof import tof_expected
        ref_tofs = tof_expected(**tof_ref_lines)
        ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[pltx],'%.0f, %.0f'%(x['ke'],x['m']),ax = ax),axis = 1)
        ref_tofs.apply(lambda x: ax.axhline(x[plty]),axis = 1)
        
        bp.plotJon.annot.vline(ax.get_xlim()[0],'[eV,amu]',ax = ax)

    if tof_mass_line !=None:
        from .tof import mass_line
        mline = mass_line(tof_mass_line)
        ax.plot(mline[pltx],mline[plty],label = 'mass line')

    return(fig,ax)
    

def tofs_scatter(thing,pltx,plty,binnum = 75,
                        bin_range = {
                                'TOF0':[.1,350],
                               'TOF1':[.1,250],
                               'TOF2':[.1,150],
                               'TOF3':[.1,50]},  
                        hist_bins = {}, 
                        fig = None,
                        ax = None,
                        logbins = False,
                        logcol =True,
                        units ='[nS]',
                        tof_ref_lines = {},
                        tof_mass_line = None):
    from pyMAP import bowPy as bp
    if hist_bins == {}:
        bins = {}
        if type(binnum) is int:
            for pl in [pltx,plty]:
                print(bin_range[pl])
                if logbins:
                    bins[pl] = np.geomspace(*bin_range[pl],binnum)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],binnum)
        elif type(binnum) is list: 
            for pl,bi in zip([pltx,plty],binnum):
                print(bin_range[pl])
                if logbins:
                    bins[pl] = np.geomspace(*bin_range[pl],bi)
                else:
                    bins[pl] = np.linspace(*bin_range[pl],bi)
    else: bins = hist_bins
    if ax is None:
        fig,ax = plt.subplots()
        fig.set_size_inches(8,6)
    
    bp.plotJon.plt.density_scatter(thing[pltx],thing[plty],
                                   ax = ax,
                                   bins = [bins[pltx],bins[plty]],
                                   log_color = logcol,
                                   alpha = .5,marker = '.')
    ax.set_xlim(min(bins[pltx]),max(bins[pltx]))
    ax.set_ylim(min(bins[plty]),max(bins[plty]))
    
    ax.set_xlabel(' '.join([pltx,units]))
    ax.set_ylabel(' '.join([plty,units]))
    if logbins:
        ax.loglog()

    if tof_ref_lines !={}:
        from .tof import tof_expected
        ref_tofs = tof_expected(**tof_ref_lines)
        ref_tofs.apply(lambda x: bp.plotJon.annot.vline(x[pltx],'%.0f, %.0f'%(x['ke'],x['m']),ax = ax),axis = 1)
        ref_tofs.apply(lambda x: ax.axhline(x[plty]),axis = 1)
        bp.plotJon.annot.vline(ax.get_xlim()[0],'[eV,amu]',ax = ax)
    if tof_mass_line !=None:
        from .tof import mass_line
        mline = mass_line(tof_mass_line)
        ax.plot(mline[pltx],mline[plty],label = 'mass line')
    return(fig,ax)
    
    