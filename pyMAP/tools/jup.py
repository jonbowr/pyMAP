import numpy as np
import pandas as pd
from ipywidgets import *


FILTERZ = {
           'Equal To':lambda x,y: np.equal(x,y),
           'Not Equal':lambda x,y:np.not_equal(x,y),
           'Greater Than': lambda x,y:np.greater_equal(x,y),
            'Less Than':lambda x,y:np.less_equal(x,y),
           'Contains (str)':lambda x,y: x.str.contains(y,na = False)
          }

def button_gen(label,button_func,button_inputs = []):
    button = widgets.Button(description=label)
    output = widgets.Output()

    display(button, output)
    button.f_out = []

    def on_button_clicked(b):
        with output:
            button.f_out.append(button_func(*button_inputs))

    button.on_click(on_button_clicked)
    return(button)

def filter_selector(df_in,group_keys = None):
    df  = df_in.reset_index()
    if not group_keys: 
        group_keys = df.keys()
    def int_call(f,append_menu = [],
                         manual = False,
                         append_func = None,
                        finp = {}):
        thing = interactive(f,{'manual': manual},**finp)
        display(thing)
        append_menu.append(append_func(thing) if append_func != None else thing)
        return(thing)
    
    def nfunc_button(selector,menu):
        p_button = button_gen('+',int_call,[selector])
        menu.append(list(p_button.f_out)[:-1])
        return(p_button)
    
    def add_filter_button(famly,group_keys):
        # Function to generate logical filter for pandas df using gui interacts
        
        fam = {}
        def log_red(Selector = { 'and':np.logical_and.reduce,
                                'or':np.logical_or.reduce,
                               'nor':np.logical_xor.reduce,
                               'not':np.logical_not.reduce},
                       fam = fixed(fam),Pick_Value = True):

            def plus_menu_button(Selector,group_keys,children,Pick_Value):
                siblings = {'menu':{}}
                
                def selector(Group = group_keys,
                                 Filter = FILTERZ,
                                 siblings = fixed(siblings),
                                 reducer = fixed(Selector),
                                 Pick_Value = fixed(Pick_Value)):
                    
                    if Pick_Value:
                        val = df[Group].dropna().unique()
                    else:
                        if np.issubdtype(df[Group].dtype, np.number):
                            val = FloatText()
                        else:
                            val = ''
                        
                    def val_pick(Value = val,
                                     Filter = fixed(Filter),
                                     siblings = fixed(siblings),
                                         group = fixed(Group)):
                        siblings['bool'] = Filter(df[group],Value)
                    menu = int_call(val_pick)
                    siblings['menu'][menu.children[0].description] = menu.children[0]
                    return(menu)

                menu = interactive(selector)
                display(menu)

                for thing in menu.children[:-1]:
                    siblings['menu'][thing.description] = thing
                children.append(siblings)
                return(menu)
            
            fam['children'] = []
            plus_button = button_gen('+',plus_menu_button,
                            [Selector,group_keys,fam['children'],Pick_Value])
            return(plus_button.f_out)
        filt_top = int_call(log_red)
        fam['parents'] = filt_top.children[0]
        famly.append(fam)
        return(filt_top)
    famly = []
    filts = []
    
    filt_button = button_gen('Add Filter',add_filter_button,
                                     [famly,group_keys])
    
    def apply_button(fams,close_stuff = [],filts = [],des = ''):

        for fam in fams:
            parent = fam['parents']
            des += '\n%s  \n{'%parent._options_labels[parent.index]
            fam_filt = []
            for sib in fam['children']:
                fam_filt.append(sib['bool'])
                labs = {}
                for l,s in sib['menu'].items():
                    if type(s) == Dropdown:
                        labs[l] = s._options_labels[s.index]
                    else:
                        labs[l] = s.value
#                     labs[l] = s.value
                des += '\n   %s %s %s(%s),'%(
                                            labs['Group'],labs['Filter'],
                                             type(labs['Value']).__name__,
                                             str(labs['Value'])
                                            )
            des+='\n  }'
            filts.append(parent.value(fam_filt))
            
        descriptor_display.value = des.replace('\n','<br>')
        
        fams = []
        for c in close_stuff:c.close()
    
    descriptor_display = HTML()
    descriptor_txt = 'Filters Generated:'
    apply_button = button_gen('Apply',
                                apply_button,
                              [famly,filt_button.f_out,filts,
                               descriptor_txt])
    display(descriptor_display)
    
    def clear_button(famly,filt,display_descript,descriptor):
        famly.clear()
        filt.clear()
        descriptor = 'Filters Generated:'
        display_descript.value = descriptor
        
    clear_button = button_gen('Clear Filters',
                                  clear_button,
                                  [famly,filts,descriptor_display,descriptor_txt])

    return(filts,descriptor_display)
    


def s_run_plotg(s_run_loc,
                overplot = True,
                ref_nam = 'file_name',
                hist_bins = 'auto',
               auto_params = {'binw':1,'buffer':.3},
               plot_params = {'hist_plt':['TOF2','TOF0','TOF1','TOF3']},
               clean_params = {},
               home = './',
               ref_mass = [1,10],
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
            
            tofs_ideal = tof_expected(ref_ke,mass = ref_mass)
            bins = {}
            for val in plot_params['hist_plt']:
                bin_start = np.min(tofs_ideal[val].values*(cpt-auto_params['buffer']))
                print(bin_start)
                if bin_start <0:
                    bin_start = 0
                bin_stop = np.max(tofs_ideal[val].values*(cpt+auto_params['buffer']))
                print(bin_stop)
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
                                eng_line = True,
                                ):
            
            checksum = float(checksum)
            clean_params = {'remove_delay':remove_delay,
                            'filt_triples':filt_triples,
                            'checksum':checksum,
                            'filt_speed':filt_speed,
                            'tof3_picker':(None if ~tof3_picker else 'auto')}

            group = pd.concat([s_s_run.loc[group_dict[v]] for v in Plot_values])
            
            species = [float(m) for m in ref_mass.split(',')]
            
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
                                ref_mass = species,
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
                            vline(loc,'%.0fkeV,%sAMU: %.1fns'%(e,spec,loc),ax = a,rot = 20)
                        elif spec_line:
                            vline(loc,'%sAMU: %.1fns'%(spec,loc),ax = a,rot = 20)
                        elif eng_line: 
                            vline(loc,'%.0fkeV: %.1fns'%(e,loc),ax = a,rot = 20)
                        if logy:
                            a.semilogy()
                        if logx:
                            a.semilogx()
                        if legend:
                            a.legend()

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
    sms_run = s_run.iloc[ll].dropna(subset = ['species'])
    jj.buttons.button_gen('plot',group_plot,[sms_run,group_keys])
#     interact(update_update)