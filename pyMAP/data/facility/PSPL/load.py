import pandas as pd
import numpy as np

def load_abm_v1(loc):    
    df = pd.read_csv(loc,usecols = range(6))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['effic'] = df['COIN Rate']**2/(df['OUT CEM Rate']*df['IN CEM Rate'])
    df['abs_mean'] =df['COIN Rate']/df['effic'] 
    
    return(df.set_index('Start Time'))

def load_motion_control_v1(loc):
    df = pd.read_csv(loc,header = 1)
    df['Time'] = pd.to_datetime(df['Time'])
    return(df.set_index('Time'))

def load_ion_source_operate_v1(loc):
    cols = ['Timestamp','Beam Energy [V]', 'Focus 1 [V]',
       'Focus 2 [V]', 'Emission Current [mA]', 'Extractor Voltage [%]',
       'Scan Position X (PX) [mm]', 'Scan Position Y (PY) [mm]',
       'Scan Area dX [mm]', 'Scan Area dY [mm]',  'Wien Filter State',
       'Wien Filter Plate Control', 'Magnet Type',
       'Wien Filter Plate Potential [V]', 'Lens In [V]', 'Lens Out [V]',
       'Error Codes', 'Warning Codes', 'Remote Control Status',
       'Precision Leak Steps',
       'Matsusada Output Voltage (V)', 'Matsusada Monitored Voltage (V)',
       'Matsusada Monitored Current',
       ' Beamline Voltage Total (Ion Source + Matsusada Output) (V)']
    df = pd.read_csv(loc,header = 1,on_bad_lines='warn').dropna(axis = 0,thresh = 3)[cols]

    df['dateTime'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('dateTime')
    df.index = df.index.tz_localize('US/Eastern').tz_convert('UTC')
    
    return(df)

def load_sample_pressures(loc):
    #PSPL CAL System Data Columns.txt from mitchell 11/26/2024
    scols = 'A: Time Stamp,B: Main Chamber Pressure,D: Flight Tube Pressure,F: Ion Turbo Pressure,H: Ion Source Pressure,X: Charge Exchange Pressure'
    abc_cols = [thing[0] for thing in scols.split(',')]
    icols =  [ord(char.lower()) - 96 -1 for char in abc_cols]
    lab_cols= [thing.split(':')[1].strip() for thing in scols.split(',')]
    

    # df = pd.read_csv(loc,usecols = icols,header = None,names = lab_cols)
    def parse_pressure(x):
        if x == 'OFF':
            return(np.nan)
        else:
            return(float(x.replace('mTorr','E-3').replace('Torr','').replace(' ','')))
    # Pick out every 5th sec of data to parse down size
    chunk_size = 5000
    selected_rows = []
    for chunk in pd.read_csv(loc,usecols = icols,header = None,
                             names = lab_cols, chunksize=chunk_size,
                             converters = {lab:parse_pressure if 'pressure' in lab.lower() else None for lab in lab_cols}):
        # Select every 5th row from the chunk
        selected_rows.append(chunk.iloc[::5])
    df = pd.concat(selected_rows,ignore_index = True)

    df['dateTime'] = pd.to_datetime(df['Time Stamp'])
    df = df.set_index('dateTime')
    df.index = df.index.tz_localize('US/Eastern').tz_convert('UTC')
    
    return(df)

loadlib = {
            'ABM-Counts':load_abm_v1,
            'Motion-System-Control':load_motion_control_v1,
            'Ion-Source-Operate':load_ion_source_operate_v1,
            'System-Monitoring-Log':load_sample_pressures
            }

def load(as_runloc,dtype = 'strSen',version = 'v001'):
    print(as_runloc)
    # try:
    df = loadlib[dtype](as_runloc)
    return(df)
    # except:return(np.nan)
