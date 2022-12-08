from datetime import datetime as dt
from datetime import timedelta
import time
import numpy as np
import pandas as pd


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