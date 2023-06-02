import numpy as np
import os

volt_scale_facts = np.array([0.0347,0.0670,0.1287,0.2533,0.4884,1.0000,1.9378])
cent_eng = np.array([14,27,52,102,197,451,908])
e_loss = np.array([0.7553,0.7576,0.7522,0.7364,0.7482,0.7295,0.7071])

sim_input = {
        'ibex':
                {
                    'volt_dict':{'Conversion Surface': -415,
                                 'P2 Electrode': -482,
                                 'P3 Electrode': 0,
                                 'Inner ESA': 816,
                                 'Outter Esa': 0,
                                 'P9 Electrode': -167,
                                 'P10 Electrode': 1212,
                                 'collimator': 0,
                                 'Rejection electrode inner radius': 0,
                                 'Rejection electrode outer radius': 0,
                                 'Optics deck and CS ground can.': 0,
                                 'TOF_PAC_VOLTAGE': 16000,
                                 'TOF_PAC_+1kV_VOLTAGE': 16000,
                                 'MCP Plane': 16000},
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IBEX',
                    'gemfil':'IBEX-Lo_CR3_CE6_TOF3_HK3.GEM',
                },
        'imap1':
                {
                    'volt_dict':{'Collimator': 0.0,
                                'Inner Rejection Electrode': 4000.0,
                                'Outer Rejection Electrode': -3500.0,
                                'Conversion Surface': -811.6,
                                'P2 Electrode': -879.4,
                                'P3 Electrode': 0.0,
                                'P9 Electrode': -161.0,
                                'Inner ESA': 1235.3,
                                'P10 Electrode': 1782.4,
                                'TOF PAC': 16000.0},
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IMAP',
                    'gemfil':[
                            # 'gem/splitup/IMAP-Lo_MAG1_HK6.GEM',
                                # 'gem/splitup/IMAP-Lo_CR7_HK6.GEM',
                                'gem/splitup/IMAP-Lo_CE12_TOF2_HK6.GEM'],
                },
        'imap7':
                {
                    'volt_dict':{'Collimator': 0.0,
                                 'Conversion Surface': -362.73,
                                 'P2 Electrode': -393.03,
                                 'P3 Electrode': 0.0,
                                 'P9 Electrode': -71.996,
                                 'Inner ESA': 804.11,
                                 'P10 Electrode': 1160.24,
                                 'TOF PAC': 16000.0},
                    'home':r'C:\Users\Jonny Woof\OneDrive - USNH\Box\Research\Projects\IMAP\simulations\IMAP-lo_ESA_CS_sims\IMAP',
                    'gemfil':[
                                # 'gem/splitup/IMAP-Lo_MAG1_HK6.GEM',
                                # 'gem/splitup/IMAP-Lo_CR7_HK6.GEM',
                                'gem/splitup/IMAP-Lo_CE12_TOF2_HK6.GEM']
                }
        }

cs_locs = {
                'ibex':{'first':np.array([99.4,133,0]),'last':np.array([158.9,116.8,0])},
                'imap1':{'first':np.array([100.5,134.6,0]),'last':np.array([160,118.4,0])},
                'imap7':{'first':np.array([100.5,134.6,0]),'last':np.array([160,118.4,0])}
            }

