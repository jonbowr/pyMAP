import pandas as pd
import numpy as np
import os

def load_cal_data(dloc = 'auto',index_cols = 8,data_cols = 20):
    # locate the scattering data
    if dloc == 'auto':
        lpath = os.path.dirname(__file__)
        for up in range(2):
            lpath = os.path.dirname(lpath+'..')

        f_cs_data = os.path.join(lpath,"cal/cal_results/CS_Ilena_Scattering_Results.xlsx")
    else: f_cs_data = dloc

    #import the scattering data
    hframe = pd.read_excel(f_cs_data,usecols = np.arange(index_cols,data_cols),
                                    nrows = 5)[3:].T
    # define header and reduce
    hframe.values[:,1] = hframe.values[:,1]/2
    head = pd.MultiIndex.from_frame(hframe,names = ['fit','energy'])

    cal = pd.read_excel(f_cs_data,usecols = np.arange(data_cols),header = 5).dropna(thresh = 3)
    nams = ['geo','sample','coating','roughness','location','incident_angle','species','recoil_props']
    cal[nams] = cal[nams].fillna(method = 'ffill')
    cal.set_index(nams,inplace = True)
    cal.set_axis(head,axis = 1,inplace = True)
    for group in ['automatic','contour']:
        for val in cal[group].columns:
            cal[(group,val)] = pd.to_numeric(cal[(group,val)],errors='coerce')
    
    # average the cal data for two FWHM finding routines (automatic and contour)
    #   and over all tested CS locations
    cal = cal.stack('energy').unstack('location').mean(axis =1).unstack()
    # drop unneded columns
    cal = cal.reset_index(['roughness','coating'],drop = True)
    return(cal)

def setup_cal_data(cal,
                    use_species=['H','O'], 
                         ibex_samples=['xxx','L109'], 
                         imap_samples = ['036b',39] ):
    #Perform some pre-processing to get the cal data in a format we want
    #   cal: cs scattering data to setup
    #   use_species: the species we will be analyzing
    #   ibex_samples: Ibex sample effic and scattering distributions to use
    #   imap_samples: Ibex sample effic and scattering distributions to use

    #calculate angular scale factors to convert 8 deg to 15 deg
    angs = (cal.stack().unstack(level = 'incident_angle')[15]/cal.stack().unstack(level = 'incident_angle')[8]).unstack()
    angs_15 = angs.groupby(['recoil_props','species']).mean().drop('effic')
    angs_convert = angs_15.mean(axis = 1).unstack(level = 'recoil_props')
    angs_convert['effic'] = 1
    angs_convert = angs_convert.unstack()

    # drop the 15 deg incident angle observations
    cal_sml = cal.drop(15,level = 'incident_angle').reset_index(level = 'incident_angle',drop= True)  
    # Pick out the desired samples to use in simulations
    use_samples = cal.loc[np.logical_or.reduce([\
                        np.logical_and(\
                               cal.reset_index()['geo']==g,
                               cal.reset_index()['sample']==v)\
                                          for g,samp in zip(['ibex','imap'],
                                                    [ibex_samples,imap_samples])\
                                          for v in samp])]
    # average scattering data for similar geometries
    use_dat = use_samples.groupby(['geo','species','recoil_props']).mean()
    # Scale scattering data up to 15 deg
    use_dat = use_dat.groupby(['geo','species','recoil_props']).apply(\
                lambda x: angs_convert.loc[x.reset_index()['recoil_props'],
                                           x.reset_index()['species']].values[0]*x)
    #pick out species to use in simulation
    return(use_dat.stack().unstack('species')[use_species].stack().unstack('energy'))

# Setup the fit functions
def setup_fit_funcs(use_dat,cent_eng,e_loss):
    def thing(xx):
        x = xx.dropna()
        fde = bp.Jonda(xy_data = np.stack([x.keys(),x.values]),func = 'linear')
        fde.fit_xy(use_err = False)
        return(fde)
    #linear fit all the scattering data
    fits = use_dat.apply(thing,axis =1 )

    #Add energy loss, assuming here that the energy loss for all species and surfaces are the same
    fde = bp.Jonda(xy_data = np.stack([cent_eng,e_loss]),func = 'linear')
    fde.fit_xy(use_err = False)
    fits = fits.unstack(level = 'recoil_props')
    fits['e_loss'] = [fde]*len(fits)
    fits = fits.stack()
    return(fits)