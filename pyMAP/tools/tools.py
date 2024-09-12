import numpy as np
import pandas as pd


def gauss_filt_nan(arr, sigma,mode = 'constant'):
    from scipy import ndimage
    """Apply a gaussian filter to an array with nans.

    Intensity is only shifted between not-nan pixels and is hence conserved.
    The intensity redistribution with respect to each single point
    is done by the weights of available pixels according
    to a gaussian distribution.
    All nans in arr, stay nans in gauss.
    """
    nan_msk = np.isnan(arr)

    loss = np.zeros(arr.shape)
    loss[nan_msk] = 1
    loss = ndimage.gaussian_filter(
            loss, sigma=sigma, mode=mode, cval=1)

    gauss = arr.copy()
    gauss[nan_msk] = 0
    gauss = ndimage.gaussian_filter(
            gauss, sigma=sigma, mode=mode, cval=0)
    gauss[nan_msk] = np.nan

    gauss += loss * arr

    return gauss

def concat_combine(list_df,interper = 'time'):
    return(pd.concat(list_df).sort_index().interpolate(interper).drop_duplicates().dropna())

def combiner(base,other_in, usecol = 'index'):
    # use np.in1d to combine values between data frames
    def rng_norm(arr):
        return((arr-min(arr))/(max(arr)-min(arr)))
    
    if type(other_in) != list:
        other_IT = [other_in]
    else: 
        other_IT = other_in
        
    dat_parts = [base.reset_index()]
    for other in other_IT: 
        if usecol == 'index':
            base_id = base.index
            other_id = other.index
        elif usecol == 'index_norm':
            base_id = rng_norm(base.index)
            other_id = rng_norm(other.index)
        else: 
            base = base.sort_values(usecol)
            other = other.sort_values(usecol)
            base_id = base[usecol]
            other_id = other[usecol]
        dat_parts.append(other.iloc[np.digitize(base_id,other_id)-1].reset_index().drop(
                                                    columns = (other_id.name if usecol == 'index' else usecol)))
    return(pd.concat(dat_parts,axis = 1))

def bin_find(x, bins = 50,find_val = 'peak',weights = None):
    from pyMAP.bowPy import Jonda
    fitr = Jonda(data = x,bins = bins,weights = weights)
    fitr.bin_data()
    fitr.interp_xy(kind = 'cubic')
    return(fitr.find_xy(find_val))
