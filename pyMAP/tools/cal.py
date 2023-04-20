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
    test_label = '%s_%s-%s_%s'%(instrument_version,
                                    test_name,
                                    test_index,
                                    test_facility)
    import os
    from shutil import copytree

    # Copy test DB filestructure over
    lpath = os.path.dirname(__file__)
    for up in range(2):
        lpath = os.path.dirname(lpath+'..')
    copytree("%s/cal/Test_Repo"%lpath,loc+test_label)

    # Rename subdocuments
    default_docs = [
                    'AsPlanned.xlsx', 
                    'AsRun.xlsx', 
                    'IMAP_lo_TestProcedure.doc', 
                    'TestPlan.docx', 
                    'TestReport.docx'
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
    data = tools.concat_combine(dats,'time').rolling(rolling).median()
    # data = tools.combiner(dats[0],dats[1:],'SHCOARSE')
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