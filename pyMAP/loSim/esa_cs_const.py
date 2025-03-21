import numpy as np
import os

volt_scale_facts = np.array([0.0347,0.0670,0.1287,0.2533,0.4884,1.0000,1.9378])
cent_eng = np.array([14,27,52,102,197,451,908])
e_loss = np.array([0.7553,0.7576,0.7522,0.7364,0.7482,0.7295,0.7071])

# def sim_input(geo = 'imap',vMode = 'imap_hiTh'):

def geos(): 
    from pandas import Series
    import os
    # f_gem_loc = os.path.join(lpath,"cal/cal_results/CS_Ilena_Scattering_Results.xlsx")
    # home = r'C:\Users\Jonny Woof\Documents\simPyon\IMAP-lo_ESA_CS_sims\IMAP'
    home = os.path.join(os.getenv('APPDATA'),'pyMAP')
    if not os.path.exists(home):
        os.makedirs(home)
    lpath = os.path.dirname(__file__)
    return({
        'ibex':
                {
                    'home':r'C:\Users\Jonny Woof\Documents\simPyon\IMAP-lo_ESA_CS_sims\IBEX',
                    'gemfil':'IBEX-Lo_CR3_CE6_TOF3_HK4.GEM',
                },
        'imap':
                {
                    'home':home,
                    'gemfil':[
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_CE13_TOF2_HK6.GEM'),
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_CR8_HK6.GEM'),
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_MAG1_HK6.GEM'),              
                                ],
                },
          'loV2':
                {
                    'home':home,
                    'gemfil':[
                                os.path.join(lpath,'/IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_CE13_TOF2_HK6.GEM'),
                                os.path.join(lpath,'/IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_MAG1_HK6.GEM'),          
                                ],
                    # 'pa':[ 'gem/IMAP-Lo_CR8_CE13_TOF2_HK6/100-07-1615_FM PreCal 1 Mask_Rev-.PA#'],
                    # 'pa_info':{'pa_offset_position': Series({'x':188,'oy':170,'oz':170,'rt':25})}
                },
        'imap_full':
                {
                    'home':home,
                    'gemfil':[
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_CE13_TOF2_HK6.GEM'),
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_CR8_HK6.GEM'),
                                os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP-Lo_MAG1_HK6.GEM'),              
                                ],
                    'pa':[ os.path.join(lpath,'IMAP-Lo_CR8_CE13_TOF2_HK6/IMAP Lo Collimator_20230921.PA#')],
                    'pa_info':{'pa_offset_position': Series({'x':183,'y':-157,'z':-157})}
                },
        })

# def sim_interpolators(geo,volt_config):
#     interpolators = {
#                         'loV2':{
#                                 'HiTh': 
#                                 'HiRes':
#                                 }

#                     }
#     return(interpolators[geo][volt_config])

def v_modes():
    import pandas as pd
    lpath = os.path.dirname(__file__)
    for up in range(2):
        lpath = os.path.dirname(lpath+'..')
    f_step_data = os.path.join(lpath,"pyMAP/loSim/IMAP_lo_voltage_stepping_table_reduced.xlsx")
    v_modes = pd.read_excel(f_step_data,usecols = range(9),header = 2,index_col = [0,1] )
    return(v_modes)

def sim_input(geo = 'imap',mode = 'imap_hiTh',estep = 6):
    estep_table = v_modes()
    out_put = dict(geos()[geo])
    out_put['volt_dict'] = dict(estep_table[estep][mode])
    print(out_put['volt_dict'])
    out_put['home'] = os.path.relpath(out_put['home'])
    return(out_put)

cs_locs = {
                'ibex':{'first':np.array([99.4,133,0]),'last':np.array([158.9,116.8,0])},
                'imap':{'first':np.array([100.5,134.6,0]),'last':np.array([160,118.4,0])},
                'imap_full':{'first':np.array([100.5,134.6,0]),'last':np.array([160,118.4,0])},
                }

obs_regions = {

                'imap':{
                    'TOF':{'X_MAX': 81,
                            'X_MIN':72,
                            'R_MAX':45.1,
                            'R_MIN':35.4,
                            'TOF_MEASURE':True,
                            'R_WEIGHT':False},
                    'CS':{'X_MAX': 160,
                            'X_MIN':98,
                            'R_MAX':134.6,
                            'R_MIN':117.4,
                            'TOF_MEASURE':False,
                            'R_WEIGHT':False}
                            },
                'imap_full':{
                    'TOF':{'X_MAX': 81,
                            'X_MIN':72,
                            'R_MAX':45.1,
                            'R_MIN':35.4,
                            'TOF_MEASURE':True,
                            'R_WEIGHT':False},
                    'CS':{'X_MAX': 160,
                            'X_MIN':98,
                            'R_MAX':134.6,
                            'R_MIN':117.4,
                            'TOF_MEASURE':False,
                            'R_WEIGHT':False}
                            },
                'ibex':{
                    'TOF':{'X_MAX': 81,
                            'X_MIN':72,
                            'R_MAX':45.1,
                            'R_MIN':35.4,
                            'TOF_MEASURE':True,
                            'R_WEIGHT':False},
                    'CS':{'X_MAX': 158.9,
                            'X_MIN':99.4,
                            'R_MAX':133,
                            'R_MIN':116.8,
                            'TOF_MEASURE':False,
                            'R_WEIGHT':True}
                            }
                }