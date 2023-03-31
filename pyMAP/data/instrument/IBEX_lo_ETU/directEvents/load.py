import numpy as np
import pandas as pd

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

def load(fil,
            use_filt = ['TOF0','TOF1','TOF2','TOF3'],
            filt_triples = False,
            apply_checksum = False,
            tof3_picker = None,
            min_tof = None,tof_ac = True):

    head = cal_headder(fil)
    # print(head)
    athing = pd.read_csv(fil,comment = '#',delim_whitespace= True,header = None,names = head)
    # return(athing)
    athing['tof0_sh'] = athing['TOF0']+athing['TOF3']/2
    athing['tof1_sh'] = athing['TOF1']-athing['TOF3']/2
    if tof_ac:
        from .tof import remove_delay_line as rdl
        tof_real = rdl(*athing[['TOF0','TOF1','TOF2','TOF3']].T.values)
        for lab,v in tof_real.items(): 
            # print(v)
            athing[lab] = v 

    log_good = [np.ones(len(athing)).astype(bool)]

    if apply_checksum:
        log_good.append(checksum(athing,check_max = 1))
    if filt_triples:
        for stuff in athing.keys():
            # print(stuff)
            if 'validtof' in stuff.lower():

                # print(stuff)
                log_good.append(athing[stuff].values.astype(bool))
    if min_tof:
        for stuff in use_filt:
            log_good.append(athing[stuff]>min_tof)
    
    
    if type(tof3_picker)== str and tof3_picker.lower() == 'auto':
        bb = int(np.sum(np.logical_and.reduce(log_good))/5)
        h,bins = np.histogram(athing.loc[np.logical_and.reduce(log_good)]['TOF3'],
                              (bb if bb > 2 else 5))
        bm = (bins[1:]+bins[:-1])/2
        p = bm[np.argmax(h)]
#         print(p)
        log_good.append(athing['TOF3']>p-1.5)
        log_good.append(athing['TOF3']<p+1.5)
    elif type(tof3_picker) == int:
        p = tof3_picker*4
        log_good.append(athing['TOF3']>p-1.5)
        log_good.append(athing['TOF3']<p+1.5)
    return(athing.loc[np.logical_and.reduce(log_good)])