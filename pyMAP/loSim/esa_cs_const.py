import numpy as np
import os

volt_scale_facts = np.array([0.0347,0.0670,0.1287,0.2533,0.4884,1.0000,1.9378])
cent_eng = np.array([14,27,52,102,197,451,908])
e_loss = np.array([0.7553,0.7576,0.7522,0.7364,0.7482,0.7295,0.7071])

# def sim_input(geo = 'imap',vMode = 'imap_hiTh'):

geos = {
        'ibex':
                {
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IBEX',
                    'gemfil':'IBEX-Lo_CR3_CE6_TOF3_HK3.GEM',
                },
        'imap':
                {
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IMAP',
                    'gemfil':[
                                'gem/IMAP-Lo_CR7_CE13_TOF2_HK6/IMAP-Lo_CE13_TOF2_HK6.GEM',
                                'gem/IMAP-Lo_CR7_CE13_TOF2_HK6/IMAP-Lo_CR7_HK6.GEM',
                                'gem/IMAP-Lo_CR7_CE13_TOF2_HK6/IMAP-Lo_MAG1_HK6.GEM',              
                                ],
                },
          'loV2':
                {
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IMAP',
                    'gemfil':[
                                'gem/IMAP-Lo_CR7_CE13_TOF2_HK6/IMAP-Lo_CE13_TOF2_HK6.GEM',
                                'gem/IMAP-Lo_CR7_CE13_TOF2_HK6/IMAP-Lo_MAG1_HK6.GEM',              
                                ],
                },
        }

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
    out_put = dict(geos[geo])
    out_put['volt_dict'] = dict(estep_table[estep][mode])
    return(out_put)

cs_locs = {
                'ibex':{'first':np.array([99.4,133,0]),'last':np.array([158.9,116.8,0])},
                'imap':{'first':np.array([100.5,134.6,0]),'last':np.array([160,118.4,0])},
                }

obs_regions = {
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
                        'R_WEIGHT':True}
                }