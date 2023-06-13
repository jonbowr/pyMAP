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
    hframe.values[:,1] = hframe.values[:,1]/2
    head = pd.MultiIndex.from_frame(hframe,names = ['fit','energy'])

    cal = pd.read_excel(f_cs_data,usecols = np.arange(data_cols),header = 5)
    nams = ['geo','sample','coating','roughness','location','incident_angle','species','recoil_props']
    cal[nams] = cal[nams].fillna(method = 'ffill')
    cal.set_index(nams,inplace = True)
    cal.set_axis(head,axis = 1,inplace = True)
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
    from pyMAP.pyMAP.tof import v_00
    # Calculate the perpendicular velocity component from the 
    v = v_00(m_amu,ke)/10**-9/10**6
    return(np.sin(ang*np.pi/180)*v)


def vperp_av_data(cal,samples= ['036b',39,'100P','40P','xxx','L109'],
                                   mass_split = 10,v_bins = np.linspace(0,90,45)):
    # use cal data and desired samples to express scattering fwhm distributions using v_perp
    # rather than ke. scattering distributions should be linear in this form

    # select sample data to be used in determination of cs scattering effects
    sml_cal = cal.stack().unstack(['sample','geo'])[samples].mean(axis = 1)
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
    
    # average sample data and transform to a shape to allow for simple linear fitting
    sml_cal.set_index(['recoil_props','v_perp','species','v_group'],inplace = True)
    sml_cal = sml_cal['val']
    sml_cal = sml_cal.reset_index('v_perp').groupby(['v_group','species','recoil_props']).mean()
    return(sml_cal.reset_index('v_group',drop = True).set_index('v_perp',append = True).sort_index().reset_index('v_perp'))

def get_cal_fits(load_data_input = {},data_av_input = {}):
    # function to load elena scattering data, linearize the desired data in v_perp
    # and perform linear fit functions
    from pyMAP import bowPy as bp

    vdat = vperp_av_data(load_cal_data(**load_data_input),**data_av_input)
    def thing(xx):
        x = xx['v_perp']
        y = xx['val']
        fde = bp.Jonda(xy_data = np.stack([x,y]),func = 'linear')
        fde.fit_xy(use_err = False)
        fde.name = xx.name
        return(fde)    
    fits = vdat.groupby(['species','recoil_props']).apply(thing).unstack('recoil_props')
    return(fits)

def rel_angle(theta1,phi1,theta2,phi2):
    t1 = theta1/90*np.pi/2
    t2 = theta2/90*np.pi/2
    p1 = phi1/90*np.pi/2
    p2 = phi2/90*np.pi/2
    return(90/np.pi*2*np.arccos(np.sin(t1)*np.sin(t2)+np.cos(t1)*np.cos(t2)*np.cos(p1-p2)))

class cs_scatterer:
    # Control structure for cs scattering montecarlo simulations
    
    def __init__(self,cs_elevation = 165,
                    samples= ['036b',39,'100P','40P','xxx','L109'],
                        species = 'H',
                        charge = -1):
        import simPyon as sim
        self.cal_fits = get_cal_fits(data_av_input = {'samples':samples})
        self.cs_el = cs_elevation
        self.m = perd.elements.symbol(species).mass
        self.species = species
        self.charge = charge
        self.data = None
        self.type = 'modulator'

        # assign distribution functions and cs scattering modulator functions
        self.ke = {
                   'pdf': sim.particles.pdf('poisson',{'c':0,'b':.155,'k':1}),
                    'pdf2':sim.particles.pdf('sputtered'),
                   'modulator_f': self.cal_fits['e_loss'][self.species],
                    }
        self.theta = {
                       'pdf': sim.particles.pdf('poisson',{'c':0,'b':.405,'k':1}),
                       'modulator_f': self.cal_fits['theta'][self.species],
                    }
        self.phi = {
                       'pdf': sim.particles.source('gaussian',{'mean':0,'fwhm':1}),
                       'modulator_f': self.cal_fits['phi'][self.species],
                    }
    
    
    def ke_mean(self,ke,theta,phi):
        v_perp = get_vperp(self.m,ke,abs(theta - self.cs_el))
        return(self.ke['modulator_f'](v_perp)*ke)
    
    def ke_scatter(self,ke,theta,phi):
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        mean = self.ke['modulator_f'](v_perp)*ke
        fwhm = (ke-mean)*2
        direction = -1
        new_ke = (self.ke['pdf'].sample(len(ke),0,4)-self.ke['pdf']['b'])*fwhm*direction+mean
        try:
            new_ke[new_ke<0] = self.ke['pdf2'].sample(np.sum(new_ke<0),0,.67)*ke[new_ke<0]
        except:
            new_ke = abs(new_ke)
        return(new_ke)
    
    def phi_scatter(self,ke,theta,phi):
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        phi_new =self.phi['pdf'](len(phi))*self.phi['modulator_f'](v_perp)+phi
        phi_new[phi_new>180] = phi_new[phi_new>180]-360
        phi_new[phi_new<-180] = phi_new[phi_new<-180]+360
        return(phi_new)

    def theta_scatter(self,ke,theta,phi):
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        mean = 180-(self.cs_el-rel_ang)
        # mean[mean>360] = 360-mean[mean>360]
        direction = 1
        fwhm = self.theta['modulator_f'](v_perp)
        return((self.theta['pdf'].sample(len(theta),0,4)-self.theta['pdf']['b'])*fwhm*direction+mean)

    def conv_effic(self,ke,theta,phi):
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        return(self.cal_fits['effic'][self.species](v_perp))

    def scatter(self,ke,theta,phi):
        return(self.ke_scatter(ke,theta,phi),
               self.theta_scatter(ke,theta,phi),
               self.phi_scatter(ke,theta,phi))

    def fly(self,source_df,
                good_cols = ['ion n','tof','x','y','z','r',
                                'ke','theta','phi','counts','is_start'],
                                quiet = True):
        from simPyon.simPyon.data import sim_data
        ke = source_df['ke']
        theta = source_df['theta']
        phi = source_df['phi']
        data = source_df.copy()
        data['is_start'] = True

        if type(data) != sim_data:
            data['ke'] = self.ke_scatter(ke,theta,phi)
            data['theta'] = self.theta_scatter(ke,theta,phi)
            data['phi'] = self.phi_scatter(ke,theta,phi)
            data['counts'] = self.conv_effic(ke,theta,phi)/100
            self.data = data[good_cols]
            return(self.data)
        else: 
            splat = data.df.copy()[good_cols]
            splat['ke'] = self.ke_scatter(ke,theta,phi)
            splat['theta'] = self.theta_scatter(ke,theta,phi)
            splat['phi'] = self.phi_scatter(ke,theta,phi)
            splat['counts'] = self.conv_effic(ke,theta,phi)/100
            splat['is_start'] = False
            data.df = pd.concat([data.df[good_cols],splat],
                            axis = 0).set_index('ion n',
                            append = True).sort_index().reset_index(level = 'ion n')
            self.data = data
            return(self.data)

    def fly_trajectory(self,source_df,fig,ax):
        # dat = self.fly(source_df)
        # ax.plot(dat['x'],dat['r'],'.')
        return(dat)

    def show_cal_fits(self,fig = None,axs = None):
        from matplotlib import pyplot as plt
        n = 0
        def fit_pltr(fits,ax):
            def fit_pltr(x):
                xx = np.linspace(min(x.xy[0]),max(x.xy[0]),1000)
                lin = ax.plot(*x.xy,'.-',label = x.name)[0]
                ax.plot(xx,x(xx),'--',color = lin.get_color())
            print(fits)
            fits.apply(fit_pltr)
            ax.set_ylabel(fits.name)
            ax.set_xlabel('v_perp')
            ax.legend()
        grouper = self.cal_fits.stack().groupby('recoil_props')
        if fig == None:
            fig,axs = plt.subplots(len(grouper),sharex = True)
        fig.set_size_inches(6,12)
        n = 0
        for nam,group in grouper:
            group.name = nam
            fit_pltr(group,axs[n])
            n+=1
        return(fig,axs)

