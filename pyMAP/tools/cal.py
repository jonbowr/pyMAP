import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def db_init(loc = './',
                    instrument_version = '',
                    test_name = '',
                    test_index = '',
                    test_facility = '',
                    ):
    # Basic tool to copy and populate the standard test repository to the desired location

    # Define test label based on imput
    test_label = '%s_%s_%s_%s'%(instrument_version,
                                    test_index,
                                    test_facility,
                                    test_name)
    import os
    from shutil import copytree

    # Copy test DB filestructure over
    lpath = os.path.dirname(__file__)
    for up in range(2):
        lpath = os.path.dirname(lpath+'..')
    copytree("%s/cal/Test_Repo"%lpath,loc+test_label)

    # Rename subdocuments
    default_docs = [
                    'AsRun.xlsx', 
                    ]

    for docnam in default_docs:
        os.rename(os.path.join(loc+test_label,docnam),
                  os.path.join(loc+test_label,test_label+'_'+docnam))

def db_analysis_generator(loc = './'):
    # Tool to initialize analysis notebooks for quick processing raw calibration data

    import os
    from shutil import copy
    from datetime import datetime
    import glob


    # Copy analysis notebooks over from pyMAP/cal/notebooks
    lpath = os.path.dirname(__file__)
    for up in range(2):
        lpath = os.path.dirname(lpath+'..')
    lpath = lpath+'/cal/notebooks'
    
    fils = glob.glob(os.path.join(lpath,'*.ipynb'))
    analyzer = {os.path.basename(fil):fil for fil in fils}

    print('Pick Analysis to Generate:')
    from ipywidgets import interactive
    def file_cop(analysis = analyzer):
        fil = os.path.basename(analysis)
        newfil = loc+datetime.today().strftime('%Y%m%d_')+fil
        copy(analysis,newfil)
        print('Analysis notebook generated: %s'%newfil)
    inter = interactive(file_cop,{'manual':True})
    return(inter)
    
def raw_mcp_gain(f_ILO_IFB,f_ILO_TOF_BD,f_ILO_RAW_CNT,
                 home = '../Test Data/Sensor/csv',
                 rolling = 'min',
                 plt_groups = {'tof_rate[cts/s]':['TOF0','TOF1','TOF2','TOF3','SILVER'],
                                'single_rates [cts/s]':['START_A', 'START_C', 'STOP_B0', 'STOP_B3'],
                                'Efficiency':['Eff_A','Eff_B','Eff_C','Eff_TRIP']},
                use_x = 'MCP_VM'):
    from pyMAP.pyMAP.data.load import load
    from pyMAP.pyMAP.tools import tools
    import os
    from pyMAP.pyMAP.plt import df_plot_groups
    dtypes = ['ILO_IFB','ILO_TOF_BD','ILO_RAW_CNT']
    fils = [f_ILO_IFB,f_ILO_TOF_BD,f_ILO_RAW_CNT]
    dats =[load(os.path.join(home,fil),dtype=dt)\
                                 for fil,dt in zip(fils,dtypes)]
    # data = tools.concat_combine(dats,'time').rolling(rolling).median()
    data = tools.combiner(dats[0],dats[1:],'SHCOARSE')
    fig,axs = df_plot_groups(data.reset_index().set_index(use_x).sort_index(),
                             plt_groups)

    axs[0].set_title('MCP Gain',fontsize=20)

    return(fig,axs,data)

def raw_DE_import(f_ILO_RAW_DE,
                   home = '../Test Data/Sensor/csv',
                   dtype = 'ILO_RAW_DE'):
    import os
    from pyMAP.pyMAP.data.load import load
    return(load(os.path.join(home,f_ILO_RAW_DE),
                     dtype = dtype))


################################################################################
'''
Funcitons for generating DER Curve data 
'''

def bin_makr(mode,estep,DER='DER1'):
    if mode == 'HiTh':
        scale = 1.2**(np.arange(-8,13))
    else:                 
        scale = 1.1**(np.arange(-8,13))
    
    volt_step = {'HiTh':pd.DataFrame({'U+':[61.91,119.41,229.42,451.48,870.61,1782.40,3452],
                            'U-':[30.55,58.92,113.19,222.75,429.54,879.40,1701]}),
                 'HiRes':pd.DataFrame({'U+':[40.30,77.73,149.34,293.89,566.72,1160.24,2248.26],
                            'U-':[13.65,26.33,50.59,99.56,191.98,393.03,761.60]})}
    if DER == 'DER1':
        things = volt_step[mode]['U+'].loc[int(estep)-1]*scale
    else: 
        things = volt_step[mode]['U+'].values
        things = np.append(things,[things[-1]*2])
    stuff = things-np.gradient(things)/2
    return(stuff)

def break_out(dat,by = 'BHV_ESA_POS_V',
                      av_out = ['BHV_ESA_POS_V','BHV_ESA_NEG_V',
                                    'rSILVER','Eff_TRIP','rTOF0','rTOF1','rTOF2',
                                  'rDE_SILVER', 'DE_Eff_TRIP', 
                                   'rDE_SILVER_H',
                                   'rDE_SILVER_D',
                                   'rDE_SILVER_O'],
                        sum_up = ['SILVER','TOF0','TOF1','TOF2','TOF3',
                                'cDE_SILVER','cDE_SILVER_H',
                                'cDE_SILVER_D','cDE_SILVER_O'],
                        v_bins = np.geomspace(10,3500,100)):
    # Group rate data according to BHV_ESA_POS_V and average the contained values
    groups = pd.cut(dat[by].values,v_bins)
    oot = dat.groupby(groups).mean()[av_out].T.stack()
    oot_sum = dat.groupby(groups).sum()[sum_up].T.stack()
    fin =pd.concat([oot,oot_sum],axis = 0).dropna() 
    fin.index.set_names('v_bins',level = -1,inplace = True)
    return(fin)

def calc_vals(dat,v_modes,):
    # calculate the voltage scale factor and incident kinetic energy
    conv_name = {'HiTh':'imap_hiTh',
                    'HiRes':'imap_hiRes'}
    oot = {}
    use_x ='BHV_ESA_POS_V'
    up_nom = dat['beam_ke']/np.round(dat['amu'])
    try:
        v_rel = up_nom/dat[use_x]*v_modes[int(dat['E_step'])][conv_name[dat['E_mode']]]['P10 Electrode']
        oot['ke_inc'] = v_rel
    except:
        oot['ke_inc'] = np.nan
    oot['volt_scale_fact'] = dat[use_x]/v_modes[6][conv_name[dat['E_mode']]]['P10 Electrode']
    return(pd.Series(oot))

def volt_builder(asrun_dat,
                    dat_col = 'sensor_dat',
                    new_index = ['e_mode','e_step','species','beam_ke'],
                    esa_mode_lab = 'E_mode',
                    Estep_lab = 'E_step',
                    esa_up_volt_lab = 'u_pos',
                    av_out = ['BHV_ESA_POS_V','BHV_ESA_NEG_V',
                                    'rSILVER','Eff_TRIP','rTOF0','rTOF1','rTOF2',
                                  'rDE_SILVER', 'DE_Eff_TRIP', 
                                   'rDE_SILVER_H','rDE_SILVER_D','rDE_SILVER_O'],
                    sum_up = ['SILVER','TOF0','TOF1','TOF2','TOF3',
                                'cDE_SILVER','cDE_SILVER_H',
                                'cDE_SILVER_D','cDE_SILVER_O']):
    # apply voltage accumulator to asrun separated run data
    from pyMAP.pyMAP.loSim import v_modes
    by_col = 'BHV_ESA_POS_V'
    stuff = asrun_dat.set_index(new_index,append = True)
    stuff = pd.concat([stuff,stuff.index.to_frame()],axis = 1).apply(lambda x:break_out(x[dat_col],
                        by = by_col,
                        v_bins = bin_makr(x['E_mode'],x['E_step'],x['u_pos']),
                        av_out = av_out,
                        sum_up = sum_up,
                        ),axis=1).stack(level = 0).stack().dropna().unstack(level = -2)
#     return(stuff)
    v_modes = v_modes()
    new_vals = pd.concat([stuff,stuff.index.to_frame()],axis = 1).T.apply(lambda x: calc_vals(x,v_modes = v_modes)).T
    stuff = pd.concat([stuff,new_vals],axis = 1)
    return(stuff.set_index('ke_inc',append = True).dropna())

    
def dat_combiner(asrun_df,dat_cols = ['ILO_RAW_CNT','ILO_APP_NHK','DE_rates'],
                        count_labs = ['SILVER','TOF0','TOF1','TOF2','TOF3',
                                                    'cDE_SILVER','cDE_SILVER_H',
                                                    'cDE_SILVER_D','cDE_SILVER_O']):
    def combiner(dats):
        stuff = pd.concat(dats,axis = 1).sort_index()
        stuff[count_labs] = stuff[count_labs].fillna(0)
        return(stuff.interpolate('time'))
    return(asrun_df.apply(lambda x: combiner(x[dat_cols].values),axis = 1))