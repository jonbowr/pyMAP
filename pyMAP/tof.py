import numpy as np
import pandas as pd
import periodictable as perd

# IBEX-lo Tof3 quadrant values, determined through calibration
tof_3_peaks = [0.6900568049562702, 4.018218774092078, 7.277728085556459, 11.991842880356202]
# electron flight time determined through simulation
t_elec = {1:4.375828,2:4.097131}
tof_dims = {'TOF0':50,'TOF1':22.5,'TOF2':27.7}

def tof_expected(ke_in=16000,
                 species = 'H',
                 mass = None,
                quadrant = 0,include_delay = False,q = 1,e_loss = 0):

    ke = np.array(ke_in).reshape(-1)
    if type(species) is str:
        species = np.array(species.split(',')).reshape(-1)
    else:
        species = np.array(species).reshape(-1)

    if mass is None:
        mass = np.array([perd.elements.symbol(spec).mass for spec in species]).reshape(-1)
    else: 
        mass = np.array(mass).reshape(-1)
        species = ['NaN']*len(mass)
    
    units = ['','[amu]','[eV]','[cm/ns]','bool','[ns]','[ns]','[ns]','[ns]']
        
    dfs = []
    for spec,m in zip(species,mass):
        tof3_expected = quadrant*4
        d_out = {thing:[] for thing in ['species','m','ke','v0','delay']+list(tof_dims.keys())+['TOF3']}

        v0 = v_00(m,ke*(1-e_loss),q)
        v1 = v0*(1-e_loss)**(1/2)
        v_t = {'TOF0':(v0+v1)/2,'TOF1':v1,'TOF2':v0}
        d_out['species'] = np.array([spec]*len(ke))
        d_out['m']=np.array([m]*len(ke))
        d_out['ke']=ke
        d_out['v0']=v0
        d_out['delay']=np.array([include_delay]*len(ke))
        for lab,val in tof_dims.items():
            tof_offset = 0
            if include_delay == True:
                if lab == 'TOF0':
                    tof_offset = -tof3_expected/2
                elif lab == 'TOF1':
                    tof_offset = tof3_expected/2
            d_out[lab]=val/v_t[lab]+tof_offset
        d_out['TOF3']=np.array([tof3_expected]*len(ke))
        dfs.append(pd.DataFrame(d_out))
    dfs = pd.concat(dfs, ignore_index = True)
    # dfs.columns = pd.MultiIndex.from_arrays([list(dfs.keys().values),units],names  =['','Units']) 
    return(dfs)
    
def v_00(m,Vinc=7000,q = 1):
    # For a given mass and voltage drop, calculates the resulting velocity in cm/nS
    amu_c = 1.66*10**-27
    cm_c = 10**6
    qVinc = Vinc*1.6*10**-19*q
    return(np.sqrt(qVinc/m*2/amu_c)/cm_c)


def delay_line_offset(tof3=tof_3_peaks):

    A = np.array([ [ 1, 1, 1, 1],
                   [-1, 1, 1, 1],
                   [-1,-1, 1, 1],
                   [-1,-1,-1, 1]])

    B = np.flip(np.array(tof3))
    d0,d1,d2,d3 =(np.linalg.inv(A).dot(B))
    b0 = np.array([0,d0,d1+d0,d2+d1+d0])
    b3 = np.array([d0+d1+d2+d3,d1+d2+d3,d2+d3,d3])

    ft3 = (lambda x,y: abs(x-y))
    return(pd.DataFrame(np.stack([np.arange(4),ft3(b0,b3),b0,b3]).T,columns = ['Q','tof3','b0','b3']))


def tof_speeds(df):
    mindt = 0
    di = tof_dims
    vs = {}
    for lab in di:
        vs[lab] = di[lab]/df[lab]
    return(vs)

# def remove_delay_line(df_in):
#     df = df_in.copy()      
#     tof0 = df['TOF0']
#     tof1 = df['TOF1']
#     tof2 = df['TOF2']
#     tof3 = df['TOF3']
    
#     from scipy.interpolate import interp1d
#     def delay_interp(tof3,d_effects):
#         f_rn = interp1d(d_effects['tof3'],d_effects['Q'],kind = 'nearest',
#                             bounds_error = False,fill_value="extrapolate")
#         return(d_effects[['b0','b3']].loc[f_rn(tof3).astype(int)]) 

#     # define the newly calculated tof values
#     delay = delay_interp(tof3,delay_line_offset())

#     df['TOF0'] = tof0-delay['b0'].values +t_elec[1]
#     df['TOF1'] = tof1-delay['b3'].values + t_elec[1]
#     df['TOF2'] = tof2+t_elec[2] - t_elec[2]

#     return(df)

def remove_delay_line(df):
    df_nd = df.copy()
    df_nd['TOF0'] =df_nd['TOF0']+df_nd['TOF3']/2 
    df_nd['TOF1'] =df_nd['TOF1']-df_nd['TOF3']/2 
    return(df_nd)

def calc_checksum(tof0,tof1,tof2,tof3):
    return((tof0+tof3-tof2-tof1))

def log_checksum(df,check_max = 1):
    return(abs(calc_checksum(*df[['TOF0','TOF1','TOF2','TOF3']].T.values))<check_max)

def log_trips(athing):
    log_good = []
    for stuff in athing:
        if 'validtof' in stuff.lower():

            # print(stuff)
            log_good.append(athing[stuff].values.astype(bool))
    return(np.logical_and.reduce(log_good))

def log_speeds(df):
    vs = tof_speeds(df)
    return(np.logical_and(vs['TOF1']<vs['TOF2'],
                          vs['TOF0']<vs['TOF2']))

def clean(df_in,
              remove_delay = True,
              filt_triples = False,
              checksum = np.inf,
              filt_speed = False,
              tof3_picker = None,

              min_tof = 0,
              min_apply = ['TOF0','TOF1','TOF2','TOF3']):
    df = df_in.copy()



    log_good = [np.ones(len(df)).astype(bool)]

    # Filter for tripples
    if filt_triples:
        log_good.append(log_trips(df))
    
    # Filter for checksum max value
    log_good.append(log_checksum(df,checksum))


    # Remove the delay line offset and electron flight time
    if remove_delay:
        df = remove_delay_line(df)
    
    # Filter for only logical ToF combinations according to ion speed
    if filt_speed:
        log_good.append(log_speeds(df))

    # Select only events from a single quadrant
    if type(tof3_picker)== str and tof3_picker.lower() == 'auto':
        bb = int(np.sum(np.logical_and.reduce(log_good))/5)
        h,bins = np.histogram(df.loc[np.logical_and.reduce(log_good)]['TOF3'],
                              (bb if bb > 2 else 5))
        bm = (bins[1:]+bins[:-1])/2
        p = bm[np.argmax(h)]
        log_good.append(df['TOF3']>p-1.5)
        log_good.append(df['TOF3']<p+1.5)
    elif type(tof3_picker) == int:
        p = tof3_picker*4
        log_good.append(df['TOF3']>p-1.5)
        log_good.append(df['TOF3']<p+1.5)


    # Select ToFs above a min ToF
    for stuff in min_apply:
        log_good.append(df[stuff]>min_tof)
    
    return(df.loc[np.logical_and.reduce(log_good)])


def calc_eff(dat):
    df = dat.copy()
    df['SILVER'] = df[df.keys().values[df.T.reset_index()['index'].str.contains('SILVER')]].sum(axis =1)
    df['STOP_B'] = df[['STOP_B0', 'STOP_B3']].sum(axis= 1)
    
    df['Eff_A0'] = df['TOF0']/df['STOP_B']
    df['Eff_A2'] = df['TOF2']/df['START_C']
    df['Eff_A'] = df['SILVER']/df['TOF1']
    
    df['Eff_C1'] = df['TOF1']/df['STOP_B']
    df['Eff_C2'] = df['TOF2']/df['START_A']
    df['Eff_C'] = df['SILVER']/df['TOF0']
    
    df['Eff_B1'] = df['TOF1']/df['START_C']
    df['Eff_B0'] = df['TOF0']/df['START_A']
    df['Eff_B'] = df['SILVER']/df['TOF2']
    
    df['Eff_TRIP1'] = df['Eff_A0']*df['Eff_C1']*df['Eff_B1']
    df['Eff_TRIP2'] = df['Eff_A2']*df['Eff_C2']*df['Eff_B0']
    df['Eff_TRIP'] = df['Eff_A']*df['Eff_C']*df['Eff_B']
    
    return(df)
