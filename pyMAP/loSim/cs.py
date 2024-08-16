import pandas as pd
import numpy as np
import os
import periodictable as perd
from .cs_cal import *
from simPyon.simPyon.data import sim_data


def rel_angle(theta1,phi1,theta2,phi2):
    t1 = theta1/90*np.pi/2
    t2 = theta2/90*np.pi/2
    p1 = phi1/90*np.pi/2
    p2 = phi2/90*np.pi/2
    return(np.abs(180/np.pi*np.arccos(np.sin(t1)*np.sin(t2)+np.cos(t1)*np.cos(t2)*np.cos(p1-p2))))

def surf_binding_sputter(E0,cosr,E_bind):
    from simPyon.simPyon.particles import pdf
    def dn_de(E,e_bind,cosr):
        return(E/(E+e_bind)**3*cosr)

    e_pdf = pdf()
    e_pdf.f = dn_de
    e_pdf.kwargs = {'e_bind':E_bind,
                    'cosr':cosr}
    return(e_pdf.sample(len(E0),0,np.max(E0)))

def recoil_sputter_inellastic(E0,E1,theta1,phi1,theta2,phi2,m1,m2,
                                    a = 1,b = 1,c =1,mean_E_loss = .15,ke_dispersion = None):
    '''
    calculation of the recoil sputtered particle energy distribution 
    - E0: incidention Neutral energy
    - E1: recoil ion energy (determined thorugh the usual way assigning a randomized energy loss process)
    - theta1: incident neutral elevation angle
    - phi1: incident neutral azimuth angle
    - theta1: recoil ion elevation angle
    - phi1: recoil ion azimuth angle
    - M1: mass of incident neutral
    - M2: mass of sputtered ion
    - mean_E_loss: average energy loss experessed as a fraction of the incident neutral energy
    '''
    mu = m2/m1
    gamma = 4*mu/(1+mu)**2
    rel_ang = rel_angle(theta1,phi1,theta2,phi2)
    cosr = np.cos(np.abs(rel_ang*np.pi/180))
    from simPyon.simPyon.particles import source
    if ke_dispersion is None:
        e_loss = source('poisson',{'a1':0,
                                            'b1':4,
                                            'c':0,
                                            'b':.4,
                                            'k':1,
                                            'fwhm':1,
                                            'mean':1,
                                            'direction':1})
        frac_loss = e_loss(len(E0))
        q = frac_loss*cosr/np.max(cosr)*E0*mean_E_loss
    else: 
        e_loss = source('pdf')
        e_loss['f'] = ke_dispersion
        e_loss['b'] = 4
        frac_loss = e_loss(len(E0))-ke_dispersion['b']+1
        q = (frac_loss*cosr/np.max(cosr)-1)*E0+E0*mean_E_loss
        # frac_loss = e_loss(len(E0))-ke_dispersion['b']
        # q = frac_loss*E0+E0*mean_E_loss
        
    c1 = 2*mu/(1+mu)**2*E0*cosr**2
    c2 = 2*cosr/(1+mu)*np.sqrt(np.abs((mu/(1+mu)*E0*cosr)**2-mu*E0*q/(1+mu)))
    c3 = -q/(1+mu)
    Er = (a*c1+b*c2+c*c3)
    return(np.abs(Er))


def Er_sputter(E0,E1,theta1,phi1,theta2,phi2,m1,m2,E_bind=6.9,surf_binding= .5):
    rel_ang = rel_angle(theta1,phi1,theta2,phi2)
    cosr = np.cos(np.abs(rel_ang*np.pi/180))
    # calculaate the recoil scattering energy for the knock on sputtered component
    Er = recoil_sputter_inellastic(E0,E1,theta1,phi1,theta2,phi2,m1,m2)
    # print(np.sum(rel_ang>90)/len(rel_ang))
    
    rel_ang[np.random.rand(len(Er))<surf_binding] = 200
    if any(rel_ang>90):
        Er[rel_ang>90]=surf_binding_sputter(E0[rel_ang>90],cosr[rel_ang>90],E_bind)
    return(Er)

def Er_ellastic(E0,E1,theta1,phi1,theta2,phi2):
    mu = m2/m1
    gamma = 4*mu/(1+mu)**2
    cosr = np.cos(rel_angle(theta1,phi1,theta2,phi2)*np.pi/180)
    return(gamma*E0*cosr**2)

class cs_scatterer:
    # Control structure for cs scattering montecarlo simulations
    
    def __init__(self,cs_elevation = 165,
                    samples= ['xxx','FM-061','FM-093','FM-110','EM-036','EM-039'],
                        species = 'H',
                        charge = -1,
                        frac_sputtered = .1,
                        surf_binding = .5,
                        geo = None):
        import simPyon as sim
        self.cal_fits = get_cal_fits(data_av_input = {'samples':samples})
        self.data = None
        self.type = 'modulator'
        self.is_sputtered = None
        self.geo = geo
        self.collision = {}
        self.scatter_type = 'statistical' #setting to 'inelastic' gives option to generate ke from inelastic scattering

        self.part = {'cs_el':cs_elevation,
                    'm':perd.elements.symbol(species).mass,
                    'species':species,
                    'charge':charge,
                    'sputtering':frac_sputtered,
                    'surf_binding':surf_binding,
                    'sputtered_m':perd.elements.symbol(species).mass}


        # assign distribution functions and cs scattering modulator functions
        self.ke = {
                   'pdf': sim.particles.pdf('poisson',{'c':0,'b':.105,'k':1}),
                   # 'pdf_sputter':sim.particles.pdf('sputtered'),
                   'modulator_f': self.cal_fits['e_loss'][self.part['species']],
                   # params for use with elastic collision
                   # 'pdf': sim.particles.pdf('poisson',{'c':0,'b':.05,'k':1}),
                   # modulator function y intercept /.75*.05
                    }
        self.theta = {
                       'pdf': sim.particles.pdf('poisson',{'c':-.075,'b':.405*2**1.6,'k':3}),
                       # 'pdf_sputter':sim.particles.source('cos',
                       #              dist_vals = {'mean':cs_elevation-90,'range':180,'a':90,'b':180,'x_min':0}),
                       # Sputtering distribution chosen so we angularly scatter around out scatter dimension while avoiding scattering
                       #    forward inth the cs floor
                      'pdf_sputter':sim.particles.source('cos',
                                    dist_vals = {'mean':1.25,'range':2.5,'a':.65,'b':2.5,'x_min':0}),
                       'modulator_f': self.cal_fits['theta'][self.part['species']],
                    }
        self.phi = {
                       'pdf': sim.particles.source('gaussian',{'mean':0,'fwhm':1}),
                       # 'pdf_sputter':sim.particles.source('uniform',
                       #              dist_vals = {'min':-90,'max':90}),
                        'pdf_sputter':sim.particles.source('cos',
                                    dist_vals = {'mean':1,'range':.75,'a':0,'b':.75,'x_min':0}),
                       'modulator_f': self.cal_fits['phi'][self.part['species']],
                    }

        # setup structure to make the mod params easily accessable
        self.params = {l:{'modulator_f':t['modulator_f'].p0} for l,t in zip(['ke','theta','phi'],
                                                                        [self.ke,self.theta,self.phi])}
        self.params['ke']['pdf'] = self.ke['pdf'].kwargs
        self.params['effic'] = self.cal_fits['effic'][self.part['species']].p0
        self.params['setup'] = self.part

    def __str__(self):
        return('%s\n'%str(type(self))+
               'Incident M:\t%.2f[AMU]\n'%self.part['m']+
               'Sputtered M:\t%.2f[AMU]\n'%self.part['sputtered_m']+
               'Sputtering:\t%.2f[%%]\n'%self.part['sputtering']+
               'Ke Scatter:\n   '+'   '.join(['%s:\n\t%s\n'%(lab,str(val))for lab,val in self.ke.items()])+
               'Theta Scatter:\n   '+'   '.join(['%s:\n\t%s\n'%(lab,str(val))for lab,val in self.theta.items()])+
               'Phi Scatter:\n   '+'   '.join(['%s:\n\t%s\n'%(lab,str(val))for lab,val in self.phi.items()])
               )
    
    def __repr__(self):
        return(str(self))

    def ke_mean(self,ke,theta,phi):
        v_perp = get_vperp(self.part['m'],ke,abs(theta - self.part['cs_el']))

        return(self.ke['modulator_f'](v_perp)*ke)
    
    def ke_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil ion ke

        v_perp = self.collision['v_perp']

        mean = self.ke['modulator_f'](v_perp)*ke
        fwhm = (ke-mean)*2
        direction = -1
        
        new_ke = (self.ke['pdf'].sample(len(ke),0,4)-self.ke['pdf']['b'])*fwhm*direction+mean
        # take the values that show up below 0 and mark them as sputtered
        neg_log = new_ke<0
        self.is_sputtered[neg_log] = True

        return(new_ke)
    
    def ke_scatter_inellastic(self,ke,theta,phi,splat_theta,splat_phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil ion ke

        v_perp = self.collision['v_perp']
        new_ke = recoil_sputter_inellastic(ke,[],
                            theta,phi,
                            splat_theta,splat_phi,
                            self.part['m'],self.part['m'],
                            # mean_E_loss = .01,
                            mean_E_loss = (1-self.ke['modulator_f'](v_perp))*.1,
                            ke_dispersion=self.ke['pdf']
                            )

        # take the values that show up below 0 and mark them as sputtered
        neg_log = new_ke<0
        self.is_sputtered[neg_log] = True
        return(new_ke)

    def phi_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil phi direction
        
        v_perp = self.collision['v_perp']

        phi_new =self.phi['pdf'](len(phi))*self.phi['modulator_f'](v_perp)+phi

        #correct for the angular ranges so simion can accept
        phi_new[phi_new>180] = phi_new[phi_new>180]-360
        phi_new[phi_new<-180] = phi_new[phi_new<-180]+360

        # take the stat determined sputtered stuff and sample the sputtered distribution
        if any(self.is_sputtered):
            spt = self.is_sputtered
            # phi_new[self.is_sputtered] = self.phi['pdf_sputter'](np.sum(self.is_sputtered))
            phi_new[spt] = self.phi['pdf_sputter'](np.sum(spt))*(phi_new[spt])
        return(phi_new)

    def theta_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil ion theta direction

        rel_ang = self.collision['rel_ang']
        v_perp = self.collision['v_perp']
        mean = self.collision['reflect']

        direction = 1
        fwhm = self.theta['modulator_f'](v_perp)

        theta_new = (self.theta['pdf'].sample(len(theta),0,4)-self.theta['pdf']['b']/self.theta['pdf']['k'])*fwhm*direction+mean
        # take the stat determined sputtered stuff and sample the sputtered distribution
        if any(self.is_sputtered):
            spt = self.is_sputtered
            theta_new[spt] = (self.theta['pdf_sputter'](np.sum(spt))*(theta_new[spt]))
            # theta_new[spt]
        return(theta_new)

    def conv_effic(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil conversion efficiency weight factor
        v_perp = self.collision['v_perp']
        return(self.cal_fits['effic'][self.part['species']](v_perp))

    def fly(self,source_df,
                good_cols = ['ion n','tof','x','y','z','r',
                                'ke','theta','phi','counts','is_start'],
                                quiet = True):
        '''
        Function which takes source distribution and applies conversion surface
          scattering processes to determine an associated recoil ion distribution
          of the same size
        source_df: DataFrame/simPyon.sim_data, length n
              Source data frame containing the incident particle velocity vector 
              v(ke,theta,phi)  containing columns [good_cols]
        good_cols: array of columns of source_df to propagate in the fly command
              columns not declared here will may be affected by scattering 
              but their values are not computed so they are dropped 
        '''
        ke = source_df['ke']
        theta = source_df['theta']
        phi = source_df['phi']
        
        data = source_df.copy()
        data['counts'] = 1
        data['is_start'] = True


        check_labs = ['tof','vx','vy','vz','ke']
        if self.data is None or ~ np.all(source_df[check_labs]==self.data.start()[check_labs]):
            if self.geo is not None:
                self.part['cs_el'] = self.geo.get_normal(data[['x','r']])+90

            self.collision['rel_ang'] = rel_angle(theta,phi,self.part['cs_el'],0)
            self.collision['v_perp'] = get_vperp(self.part['m'],ke,self.collision['rel_ang'])
            
            if self.geo is not None:        
                self.collision['reflect']= sim_data(self.geo.reflect(data))['theta']
            else:
                self.collision['reflect'] = 180-(self.part['cs_el']-self.collision['rel_ang'])
            
            
        
        # determine if ion is sputtered or not
        self.is_sputtered = np.random.rand(len(source_df))<self.part['sputtering']

        if type(data) != sim_data:
            print('normal_data')
            data['theta'] = self.theta_scatter(ke,theta,phi)
            data['phi'] = self.phi_scatter(ke,theta,phi)
            data['ke'] = self.ke_scatter(ke,theta,phi)
            data['counts'] = self.conv_effic(ke,theta,phi)/100
            self.data = data[good_cols]    
        else: 
            splat = data.df.copy()
            for k in splat.keys():
                if k not in good_cols:
                    splat.loc[:,k] =np.nan

            splat.loc[:,good_cols] = data.df[good_cols]
            splat['theta'] = self.theta_scatter(ke,theta,phi)
            splat['phi'] = self.phi_scatter(ke,theta,phi)

            if self.scatter_type == 'inelastic':
                splat['ke'] = self.ke_scatter_inellastic(ke,
                                        theta,phi,
                                        splat['theta'],splat['phi'])
            else:
                splat['ke'] = self.ke_scatter(ke,theta,phi)
            

            splat['counts'] = self.conv_effic(ke,theta,phi)/100
            splat['is_start'] = False

            # take the sputtered particles and input the coupled sputtering energy-angle distribution
            if any(self.is_sputtered):
                splat['ke'].values[self.is_sputtered] = Er_sputter(ke,splat['ke'],
                                            theta,phi,
                                            splat['theta'],splat['phi'],
                                            self.part['m'],self.part['sputtered_m'],
                                            surf_binding = self.part['surf_binding'])[self.is_sputtered]

            data.df = pd.concat([data.df,splat],
                            axis = 0).set_index('ion n',
                            append = True).sort_index().reset_index(level = 'ion n')
            self.data = data
        return(self.data.copy())

    def fly_trajectory(self,source_df,fig,ax):
        # dat = self.fly(source_df)
        # ax.plot(dat['x'],dat['r'],'.')
        return(dat)

    def show_cal_fits(self,fig = None,axs = None):
        # Function to quick visualize the modulator cal fits
        from matplotlib import pyplot as plt
        n = 0
        def fit_pltr(fits,ax):
            def fit_pltr(x):
                xx = np.linspace(min(x.xy[0]),max(x.xy[0]),1000)
                lin = ax.plot(*x.xy,'.',label = '(%s)'%','.join(x.name))[0]
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


