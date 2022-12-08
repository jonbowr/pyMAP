import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def calc_checksum(df_gt):
    return((df_gt['TOF0']+df_gt['TOF3']-df_gt['TOF2']-df_gt['TOF1']))

def checksum(df_gt,check_max = 1):
    return(np.logical_and.reduce([abs(df_gt['TOF3'])<15,
            calc_checksum(df_gt)<check_max]))

def filt_trips(athing):
    log_good = []
    for stuff in athing:
        if 'validtof' in stuff.lower():

            # print(stuff)
            log_good.append(athing[stuff].values.astype(bool))
    return(np.logical_and.reduce(log_good))

def cal_headder(fil):
    stuff = ''
    for t in open(fil).readlines():
        if '#' in t:
            stuff+=t
    head = []
    for s in stuff.split('Group')[1].split('\n'):
        sml = s.strip().strip('#').strip()
        if '.' in sml:
            try:
                hnam = sml.split('.')[1].strip(')').strip('"')
                if hnam not in head:
                    head.append(hnam)
                else:
                    head.append(hnam+'2')
            except:
                print('dat import failed: %s'%fil)
                return
    return(head)

def load(fil):
    head = cal_headder(fil)
    athing = pd.read_csv(fil,comment = '#',delim_whitespace= True,header = None,names = head)
    return(athing)


#plot the time of flights of the files
from scipy.ndimage import gaussian_filter as gf

def plot_tofs(dats,hist_plt = ['tof0_sh','tof1_sh','TOF2','TOF3'],
                        bins = {
                           'tof0_sh': np.linspace(10,350,150),
                           'tof1_sh':np.linspace(10,150,75),
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
    # fig,axs = plt.subplots(np.ceil(len(hist_plt)/1).astype(int),1,sharey = False)
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
                    # print('%.5s,%.5s'%(lab,nam))
                    # print(np.max(h)/np.mean(np.diff(bino)))
    #                 print(np.max(h))
                    
                    peak = mid[gf(np.argmax(h),2)]
    #                 ax.axvline(peak)
                    # slabel=slabel+'\n%8s:(%4.2f,%4.2f)'%(str(nam),cent,peak)
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
    # if legend_loc == 'right':
    #     ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',title = leg_lab)
    # elif legend_loc == 'below':
    #     ax.legend(loc='upper left', bbox_to_anchor=(0, -0.225),title = leg_lab)
    fig.tight_layout()

    # fig.subplots_adjust(hspace = .2,top = .925,left = .12)  
    return(fig,axs)

def plot_tofs_2d(thing,pltx,plty,binnum = 75,
                    bin_range = {
                       'tof0_sh': [10,350],
                       'tof1_sh':[10,250],
                       'TOF2':[10,150],
                       'TOF3':[0,15],
                        'TOF0': [10,350],
                       'TOF1':[10,250],},  
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
    

def s_run_plot(s_run_loc,overplot = True,ref_nam = 'file_name',
               hist_bins = 'auto',
               auto_params = {'binw':1,'buffer':.3},
               load_params = {},
               plot_params = {'hist_plt':['TOF2','TOF0','TOF1','TOF3']},
               home = './'):
    dats = s_run_get_dat(s_run_loc,ref_nam = ref_nam,
                         load_params = load_params,home = home)
#     dats = {}
#     for fil,ref_nam in zip(s_run_loc[fil_col].values,s_run_loc[ref_nam].values):
#         floc = dat_loc(str(fil).strip('.rec'),home = directory)
#         if floc:
#             dats[str(ref_nam)] = load_dt(floc,**load_params)
    
    if dats:
        if hist_bins == 'auto':
            from .tof import tof_expected
            tofs_ideal = tof_expected(np.unique(s_run_loc['ke'].values),
                                      np.unique(s_run_loc['species'].str.replace('+','')))
            bins = {}
            for val in plot_params['hist_plt']:
                vt = val.strip('_sh').lower()
                bin_start = np.min(tofs_ideal[vt].values*(1-auto_params['buffer']))
                if bin_start <0:
                    bin_start = 0
                bin_stop = np.max(tofs_ideal[vt].values*(1+auto_params['buffer']))
                if bin_start == bin_stop:
                    bin_start = 0
                    bin_stop = 100
                bins[val] = np.linspace(bin_start,bin_stop,
                                        int((bin_stop-bin_start)/auto_params['binw']) ).flatten()
                # print(bins[val].shape)
                bins['TOF3'] = np.linspace(0,15,40)
            plot_params['bins'] = bins

            fig,ax = plot_tofs(dats,**plot_params)
        return(fig,ax)

def s_run_plotg(s_run_loc,
                overplot = True,
                ref_nam = 'file_name',
                hist_bins = 'auto',
               auto_params = {'binw':1,'buffer':.3},
               load_params = {},
               plot_params = {'hist_plt':['TOF2','TOF0','TOF1','TOF3']},
               home = './',ref_spec = ['H','O'],ref_ke = [7000,16000],
               data_col = None,
               log_bins = False,cpt = 1):

    if np.any(np.isnan(np.array(ref_ke))):
        ref_ke = [7000,16000]

    # print(ref_ke)
    # print(ref_spec)
    if data_col == None:
        dats = s_run_get_dat(s_run_loc,ref_nam = ref_nam,
                             load_params = load_params,home = home)
    else:
        dats = {n:m.values[0] for n,m in s_run_loc.groupby(ref_nam).agg(
                        {data_col:lambda x: pd.concat(x.values,ignore_index =True)}).T.items()}

    if dats:
        if hist_bins == 'auto':
            from .tof import tof_expected
            tofs_ideal = tof_expected(ref_ke,ref_spec)
            bins = {}
            for val in plot_params['hist_plt']:
                vt = val.strip('_sh').lower()
                bin_start = np.min(tofs_ideal[vt].values*(cpt-auto_params['buffer']))
                if bin_start <0:
                    bin_start = 0
                bin_stop = np.max(tofs_ideal[vt].values*(cpt+auto_params['buffer']))
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


def s_run_rates(s_run_loc,overplot = True,ref_nam = 'file_name',load_params = {},rate = 'RateGold'):
    dats = s_run_get_dat(s_run_loc,ref_nam = ref_nam)
    if dats:
        plt.subplots()
        for lab,d in dats.items():
#             plt.plot(d['RateSilver'],label = lab+': Rsilver')
            plt.plot(d['Time'],d[rate],'.',label = lab+': Rgold')
        plt.legend()
#     return(dats)
#         fig.suptitle(fil_col)
#         for a in ax.flatten():


def import_srun(srun_loc):
    s_run = pd.read_excel(srun_loc,
                        header = 5,usecols = range(1,50))
    s_run.dropna(subset = ['file_name'],inplace = True)
    return(s_run)


def s_run_plot_interact(s_s_run,PlotGroups,LineGroups,
                        directory,use_data = None,
                        ref_spec_in = 'H,O',
                        ref_energies_in  = '17000',
                        ):
    from ipywidgets import FloatSlider,interact,interactive,SelectMultiple
    from .tof import tof_expected
    from bowPy.bowPy.plotJon.annot import vline


    group_dict = {str(lab):ind for lab,ind in s_s_run.groupby(PlotGroups).groups.items()}

    spec_plot = ['TOF0','tof0_sh',
                'TOF1','tof1_sh',
                'TOF2',
                'TOF3']
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
                        
                        Triples= True,
                        checksum = True,
                        norm = False,
                        peak_info = False,
                        logy = True,
                        logx = False,
                        logbins = False,
                        tof3_picker = False,
                        legend_location = 'right',
                        ref_species = ref_spec_in,ref_energies = ref_energies_in,
                        spec_line = True,
                                eng_line = True,):
            # print(Plot_values)
            # print(pd.concat([group_dict[v] for v in Plot_values]))
            group = pd.concat([s_s_run.loc[group_dict[v]] for v in Plot_values])#.dropna()

            if ref_species == 'auto':
                species = np.unique(group['species'].str.replace('+',''))
            else:
                species = ref_species.split(',')
            
            energies = np.array(ref_energies.split(',')).astype(float)

            # spec_plot = ['tof0_sh','TOF2']
            fig,ax = s_run_plotg(group,
                                ref_nam = LineGroups,
                                auto_params = {'binw':bin_ns,'buffer':buffer},
                                load_params = {'filt_triples':Triples,
                                                'apply_checksum':checksum,
                                                'tof3_picker':('auto' if tof3_picker == True else None),
                                                'min_tof':.01,'use_filt':['TOF3']
                                              },
                                plot_params = {'norm':(None if not norm else 'max'),
                                               'hist_plt':list(Plot_times),
                                               'leg_lab':LineGroups,
                                               'info':peak_info,
                                               'legend_loc':legend_location,
                                               },
                                home = directory,
                                ref_spec = species,
                                ref_ke = energies,
                                data_col = use_data,
                                cpt = window,
                                log_bins = logbins,
                                )
            print(species)
            for spec in species: 
                for e in energies:
                    # print(spec.upper()+', '+str(e))
                    tof_expect = tof_expected([e],[spec],e_loss=0)
                    print(spec_plot)
                    print(tof_expect[[s.lower().strip('_sh') for s in spec_plot]])
                    for a,loc in zip(ax.flatten(),tof_expect[[s.lower().strip('_sh') for s in Plot_times]].values.flatten()):
                        # a.axvline(loc,text_loc = 'bottom')
                        # print(e,spec,loc)
                        if spec_line and eng_line: 
                            vline(loc,'%.1feV,%s:%.1f'%(e,spec,loc),ax = a,rot = 0)
                        elif spec_line:
                            vline(loc,'%s:%.1f'%(spec,loc),ax = a,rot = 0)
                        elif eng_line: 
                            vline(loc,'%.1feV:%.1f'%(e,loc),ax = a,rot = 0)
                        if logy:
                            a.semilogy()
                        if logx:
                            a.semilogx()

            fig.suptitle('%s : %s'%(PlotGroups,Plot_values),y = 1,x = .5,ha = 'center')
    #         fig.supylabel('counts [normalized]')
            fig.text(0.04, 0.5, 'counts [norm]', va='center',ha='center', rotation='vertical',fontsize = 20)
    return(interactive(update))