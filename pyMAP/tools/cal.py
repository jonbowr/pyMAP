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

