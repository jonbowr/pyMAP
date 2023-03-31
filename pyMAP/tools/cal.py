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