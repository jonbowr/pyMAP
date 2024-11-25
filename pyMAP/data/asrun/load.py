import pandas as pd
import numpy as np
from . import asrun
from pyMAP.pyMAP.data.load import load as loader

def load_v1(f_as_run,home = './',sheet_name = 0):
    import os
    df = pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                sheet_name = sheet_name,
                header=2,
                index_col = [0,1,2,3]
                ),axis = 1).T.reset_index(level =0, drop = True ).T
    df = df.dropna(axis = 0,how = 'all')
    df = df.dropna(axis = 1,how = 'all')
    return(df)

def ETU_v1(f_as_run,home = './',sheet_name = 0):
    import os
    df = pd.concat(pd.read_excel(os.path.join(home,f_as_run),
                sheet_name = sheet_name,
                header=5,
                ),axis = 1).T.reset_index(level =0, drop = True ).T
    df = df.dropna(axis = 0,subset = ['activity','file_name'])
    df = df.dropna(axis = 1,how = 'all')
    return(df.set_index(['date','run_n','activity']))

loadlib = {'v001':load_v1,
            'ibex_lo_etu':ETU_v1,
            'imap_lo_fm':load_v1}
pages = {
        'v001':['Global',
                'M145_beam',
                'M145_system',
                'ETU_sensor',
                'ETU_tof'],
        'v002':['Global',
                'M145_beam',
                'M145_system',
                'EM_optics',
                'EM_tof',
                'Princeton_PSPL']
        }

def load(as_runloc,home = './',page_names = pages['v002'],version = 'v001',fillna = True):
    df = loadlib[version](as_runloc,home,sheet_name = page_names)

    if fillna:
        subset = np.array(['pac',
        'mcp_v',
        'mcp_v_reg',
        'TOF_mcp_v',
        'mcp_anode_thresh',
        'acc_t',
        'gas','species',
        'beam_ke',
        'voltMatsu',
        'beam_meas',
        'wein_mag',
        'Helm Enabled',
        'volt_wein',
        'voltFocus1',
        'voltFocus2',
        'beam_ext_ke',
        'Emission',
        'beamPx',
        'beamPy',
        'chrg_ex_y',
        'beamEnabled',
        'pressureChamber',
        'chamber_ig',
        'stageOuter',
        'stageInner',
        'stageX',
        'Collimator',
        'ABM'])
        use_subset = subset[[sub in df for sub in subset]]
        df[use_subset] = df[use_subset].fillna(method = 'ffill')
    return(df)