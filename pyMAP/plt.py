import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from ipywidgets import *

#plot the time of flights of the files
from scipy.ndimage import gaussian_filter as gf

def plot_tofs(dats,hist_plt = ['TOF0','TOF1','TOF2','TOF3'],
                        bins = {
                           'TOF2':np.linspace(10,150,75),
                           'TOF3':np.linspace(0,15,50),
                            'TOF0': np.linspace(10,350,150),
                           'TOF1':np.linspace(10,150,75),  
                                },
                        norm = None,leg_lab = '',info = False,
                        legend_loc='right'):
    
    if len(hist_plt)>1:
        fig,axs = plt.subplots(np.ceil(len(hist_plt)/1).astype(int),1,sharey = False)
    else:
        fig,ax = plt.subplots()
        axs = np.array([ax])
    fig.set_size_inches(9,4*len(axs))
    
    for lab,thing in dats.items():
        if info:
            # slabel = '%4s: \n     (%6s,%6s)'%(str(lab),'Mean','Peak')
            slabel = '%4s: \n%12s(%6s)'%(str(lab),' ','Peak')
        else: 
            slabel = str(lab)

        if 'TOF0' in thing:
            labs = {}
            if info:
                for nam in hist_plt:
                    cent = np.nanmean(thing[nam])
                    h,bino = np.histogram(thing[nam],bins = bins[nam])[:2]
                    mid = (bino[:-1]+bino[1:])/2
                    
                    peak = mid[gf(np.argmax(h),2)]

                    slabel=slabel+'\n%8s:(%4.2f)'%(str(nam),peak)
                
            for nam,ax in zip(hist_plt,axs.reshape(-1,1).flatten()):
                cent = np.nanmean(thing[nam])
                h,bino = np.histogram(thing[nam],bins = bins[nam])[:2]
                mid = (bino[:-1]+bino[1:])/2
                peak = mid[gf(np.argmax(h),2)]
                
                if norm == 'max':
                    ax.plot(mid,h/np.nanmax(h),alpha = .4,
                        label = slabel,)
                else:
                    ax.hist(thing[nam],bins = bins[nam],density = False,alpha = .2,
                        label = slabel,histtype = 'stepfilled')
                    ax.hist(thing[nam],bins = bins[nam],density = False,alpha = .8,
                            histtype = 'step',color = 'k')
                ax.set_xlabel('%s [nS]'%nam)
                ax.set_xlim(min(bins[nam]),max(bins[nam]))

    fig.tight_layout()

    return(fig,axs)

def plot_tofs_2d(thing,pltx,plty,binnum = 75,
                    bin_range = {
                       'TOF2':[0,150],
                       'TOF3':[0,15],
                        'TOF0': [0,350],
                       'TOF1':[0,250],},  
                            fig = None,ax = None,
                            logbins = False,logcol =True):
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
    if ax is None:
        fig,ax = plt.subplots()

    x = (bins[pltx][1:]+bins[pltx][:-1])/2
    y = (bins[plty][1:]+bins[plty][:-1])/2
    cnts = np.histogram2d(thing[pltx],thing[plty],
                          bins = [bins[pltx],bins[plty]],density = True)[0].T
    ax.pcolormesh(x,y,(np.log(cnts)if logcol else cnts))
    ax.set_xlabel(pltx)
    ax.set_ylabel(plty)
    return(fig,ax)
    

def s_run_plotg(s_run_loc,
                overplot = True,
                ref_nam = 'file_name',
                hist_bins = 'auto',
               auto_params = {'binw':1,'buffer':.3},
               plot_params = {'hist_plt':['TOF2','TOF0','TOF1','TOF3']},
               clean_params = {},
               home = './',
               ref_spec = [1,10],
               ref_ke = [7000,16000],
               data_col = 'dat_de',
               log_bins = False,
               cpt = 1):
    from .tof import tof_expected,clean

    if np.any(np.isnan(np.array(ref_ke))):
        ref_ke = [7000,16000]



    dats = {n:m.values[0] for n,m in s_run_loc.groupby(ref_nam).agg(
                    {data_col:lambda x: clean(pd.concat(x.values,ignore_index =True),
                                              **clean_params)}).T.items()}

    if dats:
        if hist_bins == 'auto':
            
            tofs_ideal = tof_expected(ref_ke,ref_spec)
            bins = {}
            for val in plot_params['hist_plt']:
                bin_start = np.min(tofs_ideal[val].values*(cpt-auto_params['buffer']))
                if bin_start <0:
                    bin_start = 0
                bin_stop = np.max(tofs_ideal[val].values*(cpt+auto_params['buffer']))
                if bin_start == bin_stop:
                    bin_start = 0
                    bin_stop = 100
                if bin_stop >350:
                    bin_stop = 350
                if log_bins:
                    bins[val] = np.geomspace(bin_start,bin_stop,
                                            int((bin_stop-bin_start)/auto_params['binw']) ).flatten()
                else:
                    bins[val] = np.linspace(bin_start,bin_stop,
                                            int((bin_stop-bin_start)/auto_params['binw']) ).flatten()
                bins['TOF3'] = np.linspace(0,15,40)
            plot_params['bins'] = bins
            fig,ax = plot_tofs(dats,**plot_params)
        return(fig,ax)

def s_run_plot_interact(s_s_run,PlotGroups,LineGroups,
                        use_data = 'dat_de',
                        ref_spec_in = '1,16',
                        ref_energies_in  = '16000',
                        ):
    from ipywidgets import FloatSlider,interact,interactive,SelectMultiple
    from pyMAP.pyMAP.tof import tof_expected
    from pyMAP.bowPy.bowPy.plotJon.annot import vline
    from pyMAP.bowPy.bowPy.plotJon.legend import legend_loc

    group_dict = {str(lab):ind for lab,ind in s_s_run.groupby(PlotGroups).groups.items()}

    spec_plot = ['TOF0','TOF1','TOF2','TOF3']

    def update(Plot_values = SelectMultiple(options = group_dict.keys()),
                Plot_times = SelectMultiple(options=spec_plot,index = [0,2]),
               # group=np.unique(s_s_run[PlotGroups].values),
                        bin_ns = FloatSlider(min=.1,max = 10,
                        step = .2,continuous_update = False,
                        value = 2),
                        window = FloatSlider(min=0,max = 2,
                                                   step = .1,continuous_update = False,
                                                   value = 1),
                        buffer = FloatSlider(min=.1,max = 2,
                                                   step = .2,continuous_update = False,
                                                   value = .7),
                        remove_delay = True,
                        filt_triples = False,
                        checksum = '99999',
                        filt_speed = False,
                        tof3_picker = False,

                        norm = False,
                        logy = True,
                        logx = False,
                        logbins = False,
                        legend = True,
                        ref_mass = ref_spec_in,
                        ref_energies = ref_energies_in,
                        spec_line = True,
                                eng_line = True,):
            
            checksum = float(checksum)
            clean_params = {'remove_delay':remove_delay,
                            'filt_triples':filt_triples,
                            'checksum':checksum,
                            'filt_speed':filt_speed,
                            'tof3_picker':(None if ~tof3_picker else 'auto')}

            group = pd.concat([s_s_run.loc[group_dict[v]] for v in Plot_values])
            if ref_mass == 'auto':
                species = np.unique(group['species'].str.replace('+',''))
            else:
                species = ref_mass.split(',')
            
            energies = np.array(ref_energies.split(',')).astype(float)
            plt.close('all')
            fig,ax = s_run_plotg(group,
                                ref_nam = LineGroups,
                                auto_params = {'binw':bin_ns,'buffer':buffer},
                                plot_params = {'norm':(None if not norm else 'max'),
                                               'hist_plt':list(Plot_times),
                                               'leg_lab':LineGroups,
                                               # 'legend_loc':legend_location,
                                               },
                                ref_spec = species,
                                ref_ke = energies,
                                data_col = use_data,
                                cpt = window,
                                log_bins = logbins,
                                clean_params = clean_params,
                                )
            
            n = 1
            for spec in species: 
                for e in energies:
                    tof_expect = tof_expected([e],mass = [int(spec)],e_loss=0)
                    e = e/1000
                    for a,loc in zip(ax.flatten(),tof_expect[[s for s in Plot_times]].values.flatten()):
                        if spec_line and eng_line: 
                            
                            vline(loc,'%.0fkeV,%s: %.1fns'%(e,spec,loc),ax = a,rot = 45)
                        elif spec_line:
                            vline(loc,'%s: %.1fns'%(spec,loc),ax = a,rot = 45)
                        elif eng_line: 
                            vline(loc,'%.0fkeV: %.1fns'%(e,loc),ax = a,rot = 45)
                        if logy:
                            a.semilogy()
                        if logx:
                            a.semilogx()

            fig.suptitle('%s : %s'%(PlotGroups,Plot_values),y = 1,x = .5,ha = 'center')
            fig.text(0.04, 0.5, 'counts [norm]', va='center',ha='center', rotation='vertical',fontsize = 20)
            fig.tight_layout()
    return(interactive(update,{'manual':True}))

def gen_gridbox(lst,n = 2):
    bxs =[HBox(lst[i:i + n]) for i in range(0, len(lst), n)]
    return(VBox(children=bxs))

def group_plot(sms_run,group_keys=None):
    if group_keys == None:
        group_keys = list(sms_run.keys()) 

    def update_update(
                    PlotGroups = SelectMultiple(options = group_keys,
                                                index = [0]
                                               ),
                      LineGroups = SelectMultiple(options = group_keys,
                                                  index = [0],
                                                 ),
                      data_col = 'dat_de',
                     ):
        s_s_run = sms_run.dropna(subset = [data_col],axis =0 )

        pltm = s_run_plot_interact(s_s_run,list(PlotGroups),
                                   list(LineGroups),use_data = data_col)
        display(gen_gridbox(pltm.children[:-1],2))
        display(pltm.children[-1])
    up = interactive(update_update,{'manual':True})
    
    display(gen_gridbox(up.children[:-2],2))
    for c in up.children[-2:]:display(c)

def filter_plot(s_run,group_keys):
    ll = jj.filters.filter_gen(s_run,group_keys)[0]
    print(np.sum(ll))
    sms_run = s_run.loc[ll].dropna(subset = ['species'])
    jj.buttons.button_gen('plot',group_plot,[sms_run,group_keys])
#     interact(update_update)