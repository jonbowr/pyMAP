import pandas as pd
import numpy as np
import os
import periodictable as perd
from .cs_cal import *

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
                                    a = 1,b = 1,c = 1,mean_E_loss = .15):
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
    e_loss = source('poisson',{'a1':0,
                                        'b1':4,
                                        'c':0,
                                        'b':.4,
                                        'k':1,
                                        'fwhm':1,
                                        'mean':1,
                                        'direction':1})
    q = e_loss(len(E0))*cosr/np.max(cosr)*E0*mean_E_loss
    c1 = 2*mu/(1+mu)**2*E0*cosr**2
    c2 = 2*cosr/(1+mu)*np.sqrt(np.abs((mu/(1+mu)*E0*cosr)**2-mu*E0*q/(1+mu)))
    c3 = -q/(1+mu)
    Er = (a*c1+b*c2+c*c3)
    return(np.abs(Er))


def Er_sputter(E0,E1,theta1,phi1,theta2,phi2,m1,m2,E_bind=6.9):
    rel_ang = rel_angle(theta1,phi1,theta2,phi2)
    cosr = np.cos(np.abs(rel_ang*np.pi/180))
    # calculaate the recoil scattering energy for the knock on sputtered component
    Er = recoil_sputter_inellastic(E0,E1,theta1,phi1,theta2,phi2,m1,m2)
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
                    samples= ['036b',39,'100P','40P','xxx','L109'],
                        species = 'H',
                        charge = -1,
                        frac_sputtered = 0):
        import simPyon as sim
        self.cal_fits = get_cal_fits(data_av_input = {'samples':samples})
        self.cs_el = cs_elevation
        self.m = perd.elements.symbol(species).mass
        self.species = species
        self.charge = charge
        self.data = None
        self.type = 'modulator'
        self.sputtering = frac_sputtered
        self.is_sputtered = None
        self.sputtered_m= 1

        # assign distribution functions and cs scattering modulator functions
        self.ke = {
                   'pdf': sim.particles.pdf('poisson',{'c':0,'b':.105,'k':1}),
                    'pdf_sputter':sim.particles.pdf('sputtered'),
                   'modulator_f': self.cal_fits['e_loss'][self.species],
                    }
        self.theta = {
                       'pdf': sim.particles.pdf('poisson',{'c':0,'b':.405,'k':1}),
                       'pdf_sputter':sim.particles.source('cos',
                                    dist_vals = {'mean':cs_elevation-90,'range':180,'a':90,'b':180,'x_min':0}),
                       'modulator_f': self.cal_fits['theta'][self.species],
                    }
        self.phi = {
                       'pdf': sim.particles.source('gaussian',{'mean':0,'fwhm':1}),
                       # 'pdf_sputter':sim.particles.source('uniform',
                       #              dist_vals = {'min':-90,'max':90}),
                       'pdf_sputter':sim.particles.source('cos',
                                    dist_vals = {'mean':0,'range':180,'a':0,'b':180,'x_min':0}),
                       'modulator_f': self.cal_fits['phi'][self.species],
                    }
    
    def ke_mean(self,ke,theta,phi):
        v_perp = get_vperp(self.m,ke,abs(theta - self.cs_el))
        return(self.ke['modulator_f'](v_perp)*ke)
    
    def ke_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil ion ke

        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        mean = self.ke['modulator_f'](v_perp)*ke
        fwhm = (ke-mean)*2
        direction = -1
        
        new_ke = (self.ke['pdf'].sample(len(ke),0,4)-self.ke['pdf']['b'])*fwhm*direction+mean
        # take the values that show up below 0 and mark them as sputtered
        neg_log = new_ke<0
        self.is_sputtered[neg_log] = True
        # if any(neg_log):
        #     new_ke[neg_log] = self.ke['pdf2'].sample(np.sum(neg_log),0,.67)*ke[neg_log]
            # new_ke[self.is_sputtered] = self.ke['pdf2'].sample(np.sum(self.is_sputtered),0,.67)*ke[self.is_sputtered]
        return(new_ke)
    
    def phi_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil phi direction
        
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        phi_new =self.phi['pdf'](len(phi))*self.phi['modulator_f'](v_perp)+phi

        #correct for the angular ranges so simion can accept
        phi_new[phi_new>180] = phi_new[phi_new>180]-360
        phi_new[phi_new<-180] = phi_new[phi_new<-180]+360

        # take the stat determined sputtered stuff and sample the sputtered distribution
        if any(self.is_sputtered):
            phi_new[self.is_sputtered] = self.phi['pdf_sputter'](np.sum(self.is_sputtered))
        return(phi_new)

    def theta_scatter(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil ion theta direction

        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        mean = 180-(self.cs_el-rel_ang)
        # mean[mean>360] = 360-mean[mean>360]
        direction = 1
        fwhm = self.theta['modulator_f'](v_perp)
        theta_new = (self.theta['pdf'].sample(len(theta),0,4)-self.theta['pdf']['b'])*fwhm*direction+mean
        # take the stat determined sputtered stuff and sample the sputtered distribution
        if any(self.is_sputtered):
            theta_new[self.is_sputtered] = self.theta['pdf_sputter'](np.sum(self.is_sputtered))
        return(theta_new)

    def conv_effic(self,ke,theta,phi):
        # Function to take ion velocity vector apply statistical sampling to determine 
        #   recoil conversion efficiency weight factor
        rel_ang = rel_angle(theta,phi,self.cs_el,0)
        v_perp = get_vperp(self.m,ke,rel_ang)
        return(self.cal_fits['effic'][self.species](v_perp))

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
        from simPyon.simPyon.data import sim_data
        ke = source_df['ke']
        theta = source_df['theta']
        phi = source_df['phi']
        data = source_df.copy()
        data['is_start'] = True

        # determine if ion is sputtered or not
        self.is_sputtered = np.random.rand(len(source_df))<self.sputtering

        if type(data) != sim_data:
            data['theta'] = self.theta_scatter(ke,theta,phi)
            data['phi'] = self.phi_scatter(ke,theta,phi)
            data['ke'] = self.ke_scatter(ke,theta,phi)
            data['counts'] = self.conv_effic(ke,theta,phi)/100
            self.data = data[good_cols]
            
        else: 
            splat = data.df.copy()[good_cols]
            splat['theta'] = self.theta_scatter(ke,theta,phi)
            splat['phi'] = self.phi_scatter(ke,theta,phi)
            splat['ke'] = self.ke_scatter(ke,theta,phi)
            splat['counts'] = self.conv_effic(ke,theta,phi)/100
            splat['is_start'] = False
            # take the sputtered particles and input the coupled sputtering energy-angle distribution
            splat['ke'][self.is_sputtered] = Er_sputter(ke,splat['ke'],
                                        theta,phi,
                                        splat['theta'],splat['phi'],
                                        self.m,self.sputtered_m)[self.is_sputtered]
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
        # Function to quick visualize the modulator cal fits
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

