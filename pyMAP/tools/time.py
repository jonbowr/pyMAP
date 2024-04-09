from datetime import datetime as dt
from datetime import datetime, timezone
from datetime import timedelta
import time
import numpy as np
import pandas as pd
import pytz

def gps_to_datetime(gps_time):

    def toYearFraction(date):
        def sinceEpoch(date): # returns seconds since epoch
            return time.mktime(date.timetuple())
        s = sinceEpoch

        year = date.year
        startOfThisYear = dt(year=year, month=1, day=1)
        startOfNextYear = dt(year=year+1, month=1, day=1)

        yearElapsed = s(date) - s(startOfThisYear)
        yearDuration = s(startOfNextYear) - s(startOfThisYear)
        fraction = yearElapsed/yearDuration

        return date.year + fraction


    return(np.array([toYearFraction(dt(1980, 1, 6)+timedelta(seconds = s)) for s in gps_time]))

def orbit_fraction(df):
    func = lambda x: (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x))
    orbit_frac = df.groupby(['orbit'],as_index = False)['time'].apply(func)
    return(df['orbit'].values+orbit_frac.values/2)

def spin_to_shcoarse(spinsec):
    return(spinsec+2**31)   

def shcoarse_to_datetime(timestanp):
    #turn start date of IMAP-LO epoch into a time stamp in seconds
    epoch=dt(2010, 1, 1, 0, 0, 0)
        
    # convert Shecoarse to spin seconds
    spin_sec = timestanp-(2**31)
    now = spin_sec+epoch.timestamp()
    date_time= dt.fromtimestamp(now)

    return date_time

def localize_to_tz(naive,zone = 'est'):
    # Set zone information
    if zone =='est':
        local=pytz.timezone('US/Eastern').localize(naive)
    elif zone=='bern':
        local=pytz.timezone('Europe/Zurich').localize(naive)
    else:
        try: 
            local=pytz.timezone(zone).localize(naive)
        except:
            raise Exception("""Please choose a valid time zone : 'est', 'bern'""")
    #return date with zone information added
    return local


def utc_to_local(utc_dt,local = 'US/Eastern'):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=local)

def get_file_times(path):
    import os
    ti_c = os.path.getctime(path)
    ti_m = os.path.getmtime(path)
     
    # Converting the time in seconds to a timestamp
    # c_ti = time.ctime(ti_c)
    # m_ti = time.ctime(ti_m)
    c_ti = dt.fromtimestamp(ti_c)
    m_ti = dt.fromtimestamp(ti_m)
    return(c_ti,m_ti)