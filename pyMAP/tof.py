import numpy as np
import pandas as pd
import periodictable as perd
from .tof_const import *

def tof_expected(ke=16000,
                    species = 'H',
                    mass = None,
                    q = 1,
                    e_loss = 0,
                    delay_quad = None,
                    instrument = 'nominal'):

    ke = np.array(ke).reshape(-1)
    # Setup species array, parse input type
    if type(species) is str:
        species = np.array(species.split(',')).reshape(-1)
    else:
        species = np.array(species).reshape(-1)

    # setup mass arrays, parse input types
    if mass == None:
        mass = np.array([(perd.elements.symbol(spec\
                         if spec != 'H2' else 'D').mass\
                             if spec != 'e' else m_elec_amu)\
                                 for spec in species]).reshape(-1)
    else: 
        mass = np.array(mass).reshape(-1)
        species = ['NaN']*len(mass)
    
    units = ['','[amu]','[eV]','[cm/ns]','bool','[ns]','[ns]','[ns]','[ns]']
        
    dfs = []
    # Loop through mass and species arrays to calculate the dataframe of ref values
    for spec,m in zip(species,mass):
        for quad in [delay_quad] if type(delay_quad)!= list else delay_quad: 
            d_out = {thing:[] for thing in ['species','m','ke','v0']+\
                                    list(tof_dims_cm.keys())+['TOF3']}
            v0 = v_00(m,ke*(1-e_loss),q)
            v1 = v0*(1-e_loss)**(1/2)
            v_t = {'TOF0':(v0+v1)/2,'TOF1':v1,'TOF2':v0}
            d_out['species'] = np.array([spec]*len(ke))
            d_out['m']=np.array([m]*len(ke))
            d_out['ke']=ke
            d_out['v0']=v0
            for lab,val in tof_dims_cm.items():
                d_out[lab]=val/v_t[lab]
            d_out['TOF3']=np.array([tof3_peaks_ns[instrument][quad]\
                             if quad != None else np.nan]*len(ke))
            dfs.append(pd.DataFrame(d_out))
    dfs = add_delay_line(pd.concat(dfs, ignore_index = True),instrument)
    return(dfs)
    
def mass_line(ke):
    return(pd.concat([tof_expected(ke,mass = m) for m in range(86)]))

def v_00(m,Vinc=7000,q = 1):
    # For a given mass and voltage, calculates the resulting velocity in cm/nS
    qVinc = Vinc*qv*q
    return(np.sqrt(qVinc/m*2/amu_c)/cm_c)

def tof_to_ke(tof,m,leg = 'TOF0',q = 1):
    # For a given tof,mass and leg, calculates the incident energy in eV
    return((tof_dims_cm[leg]/tof*cm_c)**2*amu_c*m/(2*qv*q))
    # return(np.sqrt(qVinc/m*2/amu_c)/cm_c)

def calc_checksum(tof0,tof1,tof2,tof3):
    return((tof0+tof3-tof2-tof1))

def tof_speeds(df):
    # calculates the tof speeds from the ToF dimensions in cm/ns
    # assumes a straight line trajectory
    mindt = 0
    di = tof_dims_cm
    vs = {}
    for lab in di:
        vs[lab] = di[lab]/df[lab]
    return(vs)

def calc_eLoss(df):
    vs = tof_speeds(df)
    return(vs['TOF1']**2/vs['TOF2']**2)

def delay_line_offset(tof3=tof3_peaks_ns['imap_lo_em'],times_out = False):

    A = np.array([ [ 1, 1, 1, 1],
                   [-1, 1, 1, 1],
                   [-1,-1, 1, 1],
                   [-1,-1,-1, 1]])

    B = np.flip(np.array(tof3))
    d0,d1,d2,d3 =(np.linalg.inv(A).dot(B))
    b0 = np.array([0,d0,d1+d0,d2+d1+d0])
    b3 = np.array([d0+d1+d2+d3,d1+d2+d3,d2+d3,d3])

    ft3 = (lambda x,y: abs(x-y))
    offsets = pd.DataFrame(np.stack([np.arange(4),ft3(b0,b3),b0,b3]).T,
                            columns = ['Q','tof3','b0','b3'])
    delay_times  = pd.Series([d0,d1,d2,d3],index = ['d0','d1','d2','d3'])
    return(offsets,delay_times)

def delay_shift(tof0,tof1,tof2,tof3,
                            instrument,
                            technique='signal',
                            mcp_v = 3000):
    from .tof_const import f_elec_t
    t_elec = f_elec_t(mcp_v)
    # t_elec_ns = {1:8,2:4.097131}
    if technique == 'signal':
        from scipy.interpolate import interp1d
        def delay_interp(tof3,d_effects):
            f_rn = interp1d(d_effects['tof3'],d_effects['Q'],kind = 'nearest',
                                bounds_error = False,fill_value="extrapolate")
            return(d_effects[['b0','b3']].iloc[f_rn(tof3).astype(int)]) 

        # define the newly calculated tof values
        delay = delay_interp(tof3,delay_line_offset(tof3_peaks_ns[instrument]))
        dtof0 = -delay['b0'].values + t_elec[0]
        dtof1 = -delay['b3'].values + t_elec[1]
        dtof2 = t_elec[0] - t_elec[1]
    elif technique == 'average':
        dtof0 = tof3/2
        dtof1 = -tof3/2
        dtof2 = np.zeros(len(tof3))
    return(np.nan_to_num(dtof0)*~np.isnan(tof3),
            np.nan_to_num(dtof1)*~np.isnan(tof3),
            np.nan_to_num(dtof2)*~np.isnan(tof3))

def remove_delay_line(df_in,
                        instrument = 'imap_lo_em',
                        technique = 'signal',
                        mcp_v = 3000):
    # Function to input standard DE data and output copied dataframe with new
    #   tof0,1,2 values associated with delay line removal
    # technique [str]: keyword to remove the delay effects [signal,average]
    #       signal: use calibration of delay line offset values
    #       average: standard tof3/2 techique

    df = df_in.copy()      
    tof0 = df['TOF0']
    tof1 = df['TOF1']
    tof2 = df['TOF2']
    tof3 = df['TOF3']
    # get_delay line shifts
    dtof0,dtof1,dtof2 = delay_shift(*df[['TOF%d'%q for q in range(4)]].T.values,
                                        instrument = instrument,technique=technique,mcp_v=mcp_v)
    df['TOF0'] = tof0+dtof0
    df['TOF1'] = tof1+dtof1
    df['TOF2'] = tof2+dtof2
    return(df)

def add_delay_line(df_in,
                    instrument = 'imap_lo_em',
                    technique = 'signal',):
    df = df_in.copy()      
    tof0 = df['TOF0']
    tof1 = df['TOF1']
    tof2 = df['TOF2']
    tof3 = df['TOF3']
    # get_delay line shifts
    dtof0,dtof1,dtof2 = delay_shift(*df[['TOF%d'%q for q in range(4)]].T.values,
                                        instrument = instrument,technique=technique)
    df['TOF0'] = tof0-dtof0
    df['TOF1'] = tof1-dtof1
    df['TOF2'] = tof2-dtof2
    return(df)

def get_checksum(df):
    return(calc_checksum(*[df['TOF%d'%i] for i in range(4)]))

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
    return(np.logical_and.reduce([vs['TOF1']<vs['TOF2'],
                                  vs['TOF0']<vs['TOF2'],
                                  vs['TOF1']<vs['TOF0']]))

def clean(df_in,
              remove_delay = True,
              filt_triples = False,
              checksum = np.inf,
              filt_speed = False,
              tof3_picker = None,
              min_tof = np.nan,
              min_apply = ['TOF0','TOF1','TOF2','TOF3'],
              remove_delay_input = {}):
    df = df_in.copy()

    log_good = [np.ones(len(df)).astype(bool)]

    # Filter for tripples
    if filt_triples:
        log_good.append(log_trips(df))
    
    # Filter for checksum max value
    if checksum < 999999:
        log_good.append(log_checksum(df,checksum))


    # Remove the delay line offset and electron flight time
    if remove_delay:
        df = remove_delay_line(df,**remove_delay_input)
    
    # Filter for only logical ToF combinations according to ion speed
    if filt_speed:
        log_good.append(log_speeds(df))

    # Select only events from a single quadrant
    if type(tof3_picker)== str and tof3_picker.lower() == 'auto':
        bb = int(np.sum(np.logical_and.reduce(log_good))/5)
        h,bins = np.histogram(df.iloc[np.logical_and.reduce(log_good)]['TOF3'],
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
    if min_tof>0:
        for stuff in min_apply:
            log_good.append(df[stuff]>min_tof)
    
    return(df.iloc[np.logical_and.reduce(log_good)])


def get_eff(dat):
    df = dat.copy()
    df['SILVER'] = df[df.keys().values[df.T.reset_index()['index'].str.contains('SILVER_TRIPLE')]].sum(axis =1)
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
    
    return(df.replace([np.inf, -np.inf,np.nan], 0))

def de_effic(rawDE):
    val_keys = rawDE.keys().to_series()
    dt = max(rawDE['SHCOARSE'])-min(rawDE['SHCOARSE'])
    df = rawDE[val_keys.loc[val_keys.str.contains('VALID')]].apply('sum')/dt
    
    df['SILVER'] = np.sum(log_trips(rawDE))/dt
    df['Eff_A'] = df['SILVER']/df['VALIDTOF1']
    df['Eff_C'] = df['SILVER']/df['VALIDTOF0']
    df['Eff_B'] = df['SILVER']/df['VALIDTOF2']
    df['Eff_TRIP'] = df['Eff_A']*df['Eff_C']*df['Eff_B']
    return(df)
    
def de_effic_filt(df_in,elec_ns = 15):
    rawDE = df_in.copy()
    val_keys = rawDE.keys().to_series()
    dt = max(rawDE['SHCOARSE'])-min(rawDE['SHCOARSE'])
    for n in range(3):
        rawDE['VALIDTOF%d'%n] = np.logical_and(rawDE['VALIDTOF%d'%n],
                                               rawDE['TOF%d'%n]>elec_ns) 
    df = rawDE[val_keys.loc[val_keys.str.contains('VALID')]].apply('sum')/dt
    
    df['SILVER'] = np.sum(log_trips(rawDE))/dt
    df['Eff_A'] = df['SILVER']/df['VALIDTOF1']
    df['Eff_C'] = df['SILVER']/df['VALIDTOF0']
    df['Eff_B'] = df['SILVER']/df['VALIDTOF2']
    df['Eff_TRIP'] = df['Eff_A']*df['Eff_C']*df['Eff_B']
    return(df)

def fit_tofs(df,
             tof_ranges = {'TOF0':[0,255],
                             'TOF1':[0,255],
                             'TOF2':[0,255]
                          },
                 bin_ns = 2
                ):
    import bowPy as bp
    fits = {}
    for tf in tof_ranges.keys():
        bins = np.linspace(*tof_ranges[tf],int((tof_ranges[tf][1]-tof_ranges[tf][0])*bin_ns))
        fits[tf] = bp.Jonda(data = df[tf],bins = bins)
        fits[tf].bin_data()
        fits[tf].interp_xy(kind = 'cubic')
    return(pd.Series(fits))
