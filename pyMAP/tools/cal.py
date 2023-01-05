import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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


def db_init(loc = './',test_name = ''):
    [
    'AsPlanned.xlxs',
    'AsRun.xlxs',
    'Test_Procedure.docx',
    'Test_Plan.docx',
    ]

    import os
