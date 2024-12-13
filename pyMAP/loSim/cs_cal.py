import pandas as pd
import numpy as np
import os
import periodictable as perd

def load_cal_data(dloc = 'auto',index_cols = 8,data_cols = 27):
    # Load and perform some preprocessing on elena cal data. Automatically uses package cal results
    # from pyMAP/cal/cal_results/cs_Ilena_scattering_results.xlsx if no file provided
    # Input:
    #   dloc (str): location of cal data file
    #   index_cols (int): range of columns to use for indexing (not the energy dependent dist values)
    #   data_cols (int): total range of columns to load containing data
    # Output: 
    #   cal (pandas.Dataframe): Illena calibration distribution results

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
    hframe[4] = hframe[4].astype(float)#/2
    
    head = pd.MultiIndex.from_frame(hframe,names = ['fit','energy'])

    cal = pd.read_excel(f_cs_data,usecols = np.arange(data_cols),header = 5)
    nams = ['geo','sample','coating','roughness','location','incident_angle','species','recoil_props']
    cal[nams] = cal[nams].fillna(method = 'ffill')
    cal.set_index(nams,inplace = True)
    cal = cal.set_axis(head,axis = 1, copy = False)
    for group in ['automatic','contour']:
        for val in cal[group].columns:
            cal[(group,val)] = pd.to_numeric(cal[(group,val)],errors='coerce')
    
    # average the cal data for two FWHM finding routines (automatic and contour)
    #   and over all tested CS locations
    cal = cal.stack().mean(axis = 1).unstack('location').mean(axis =1).unstack('energy')
    # cal = cal.stack('energy').unstack('location').median(axis =1).unstack()
    # drop unneded columns
    cal = cal.reset_index(['roughness','coating'],drop = True)
    return(cal)

def setup_cal_data_ke(cal,
                    use_species=['H','O'], 
                         ibex_samples=['xxx','L109'], 
                         imap_samples = ['036b',39] ):

    # Unused Codes
    #Perform some pre-processing to execute a linear energy-based extrapolation to get
    #to get 15 deg scattering distribution functions
    #   cal: cs scattering data to setup
    #   use_species: the species we will be analyzing
    #   ibex_samples: Ibex sample effic and scattering distributions to use
    #   imap_samples: Ibex sample effic and scattering distributions to use
    #calculate angular scale factors to convert 8 deg to 15 deg
    # function made laregly obselete by vperp_av_data
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

def setup_fit_funcs_ke(use_dat,cent_eng,e_loss):
    # Unused Codes
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

def get_vperp(m_amu,ke,ang):
    '''
    function to Calculate the perpendicular velocity component from particle energy mass and inc angle
    returns:
        perpendicular speed component in km/s
    '''

    from pyMAP.pyMAP.tof import v_00,mmNs_ms
    v = v_00(m_amu,ke)*mmNs_ms*10**-3 # speed converted from mm/ns to km/s
    return(np.sin(ang*np.pi/180)*v)


def vperp_av_data(cal,samples= ['036b',39,'100P','40P','xxx','L109'],
                                   mass_split = 10,v_bins = np.linspace(0,90,45)):
    # use cal data and desired samples to express scattering fwhm distributions using v_perp
    # rather than ke. scattering distributions should be linear in this form

    # select sample data to be used in determination of cs scattering effects
    sml_cal = cal.stack().unstack(['sample','geo'])[samples].stack().stack()#.mean(axis = 1)
    sml_cal.name = 'val'
    sml_cal = sml_cal.reset_index()
    # calculate the v_perp value from mass, energy and incident angle
    sml_cal['v_perp'] = sml_cal.apply(\
                    lambda x: get_vperp(perd.elements.symbol(x['species']).mass,
                                                x['energy'],x['incident_angle']),axis = 1)

    
    # define mass groups and v_groups to allow for selective averaging of the sample data
    sml_cal['m'] = sml_cal['species'].apply(lambda x: perd.elements.symbol(x).mass)
    sml_cal['m_group'] = ((sml_cal['m'].values/mass_split).astype(int)>=1).astype(int)
    sml_cal['v_group'] = np.digitize(sml_cal['v_perp'],v_bins)
    
    # return(sml_cal)#.reset_index('v_group',drop = True).set_index('v_perp',append = True).sort_index().reset_index('v_perp'))
    # average sample data and transform to a shape to allow for simple linear fitting
    sml_cal.set_index(['recoil_props','v_perp','species','v_group'],inplace = True)

    return(sml_cal.reset_index('v_group',drop = True).sort_index().reset_index('v_perp'))

    # sml_cal = sml_cal['val']
    # sml_cal = sml_cal.reset_index('v_perp').groupby(['v_group','species','recoil_props']).mean()
    # return(sml_cal.reset_index('v_group',drop = True).set_index('v_perp',append = True).sort_index().reset_index('v_perp'))


def get_cal_fits(load_data_input = {},data_av_input = {}):
    # function to load elena scattering data, linearize the desired data in v_perp
    # and perform linear fit functions
    from pyMAP import bowPy as bp

    #Rollover function taken from [wurz 2006]
    def rollover_v(xx,n_0=.0135,vc=4*10**4,a=.31):
        b=1.5
        x = xx*1000 #km/s to m/s
        return(n_0*(1-np.exp(-(x/vc)**(2*b)))*(x/vc)**(2*a))

    func_fits = {'e_loss':'linear',
                'phi':rollover_v,
                'theta':rollover_v,
                'effic':'linear'}

    vdat = vperp_av_data(load_cal_data(**load_data_input),**data_av_input)
    def thing(xx):
        x = xx['v_perp']
        y = xx['val']
        fde = bp.Jonda(xy_data = np.stack([x,y]),func = func_fits[xx.name[1]])
        fde.fit_xy(use_err = False)
        fde.name = xx.name
        return(fde)    
    fits = vdat.dropna().groupby(['species','recoil_props']).apply(thing).unstack('recoil_props')
    return(fits)


def make_f_eloss():
    eloss_vals = pd.DataFrame([0.82809887]*7 ,index = range(1,8),columns = ['Eloss'])

    from .esa_cs_const import cent_eng

    eloss_vals['ke'] = cent_eng
    eloss_vals['v_perp'] = get_vperp(1,eloss_vals['ke'],15)
    # Eloss defined 12/11/2024
    eloss_run0 = pd.Series({3 : 0.866685,
                            4 :  0.946218,
                            5 :  0.977120,
                            6 :  1.029214,
                            7:  0.950984})
    eloss_vals['eloss_1']=eloss_run0*eloss_vals['Eloss']
    #second run using polyfit of eloss values
    eloss_vals['eloss_2'] = pd.Series({3 :   0.698561,
                                        4:    0.786205,
                                        5:    0.784077,
                                        6:    0.886756,
                                        7:    0.777787})
    from pyMAP.bowPy import Jonda
    f_eloss_new =Jonda(xy_data = eloss_vals[['v_perp','eloss_2']].dropna().values.T)
    f_eloss_new.interp_xy('cubic',sigma = .9,bounds_error = False,interp_input = {'fill_value':'extrapolate'})
    
    return(eloss_vals,f_eloss_new)