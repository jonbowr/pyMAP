
import simPyon as sp

def sim_h2_dispersion(n,mean = 100,fwhm = 50):
    
    def e_diss(E0,Ed = 4.52,pm = 1,alpha = 0):
        return(E0/2+Ed/2+pm*np.sqrt(E0*Ed)*np.cos(alpha))

    E0 = sp.particles.source('gaussian',{'fwhm': fwhm,'mean': mean})(n)
    alpha = sp.particles.source('cos')(n)*np.pi/180
    pm = np.round(np.random.rand(n))*2-1
    return(e_diss(E0,Ed = 4.52,pm = pm,alpha = alpha))


def set_simulator_cal(sim, species = 'H',result = 'fin_cal1'):
    '''
    Function to setup instrument scattering simulator to calibrated values from FinalCal
    '''


    def fin_cal1_H(sim,species):
        '''
        Simulator settings defined following IMAP-Lo FM cal, 12/16/2024
        - model regression performed primarily against final cal results, 20241212-FMv3_T105_PSPL_FinalCal_DER.csv
        - model checked against IBEX-lo H final cal results and precal2 results
        - see 20241204_FinalCal_DER1 H Model Comparison.ipynb for exact definition
        '''

        def make_f_eloss():
            '''
             energy loss funciton defined following final cal 12/16/2024
             energy loss here defined in addition to inellastic scattering loss processes
            '''

            from pyMAP import bowPy as bp
            from . import cent_eng,cs_cal
            eloss_vals = pd.DataFrame([0.82809887]*7 ,index = range(1,8),columns = ['Eloss'])

            eloss_vals['ke'] = cent_eng
            eloss_vals['v_perp'] = cs_cal.get_vperp(1,eloss_vals['ke'],15)
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
            f_eloss_new = bp.Jonda(xy_data = eloss_vals[['v_perp','eloss_2']].dropna().values.T)
            f_eloss_new.interp_xy('cubic',sigma = .9,bounds_error = False,interp_input = {'fill_value':'extrapolate'})
            return(eloss_vals,f_eloss_new)
            
        if species == 'H':
            sim[1].part['surf_binding'] = .25
            sim[1].part['sputtering'] = .2
            sim.params['cs_scatter']['ke']['pdf']['b'] = .3
            sim[1].effic.p0 =sim[1].cal_fits['effic']['He'].p0*.0968*.68

            sim[1].scatter_type = 'inelastic'
            sim[1].ke['modulator_f'] = f_eloss_new
        return(sim)

    dict_cals = {
                    'fin_cal1': fin_cal1_h,
                }

    return(dict_cal[result](sim,species))


def make_f_eloss():
    import pandas as pd
    from .cs_cal import get_vperp
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

def grids_n_spokes(instrument_config = 'IMAP_flight'):
    '''
    Function to get dict of grid/spoke trans
    Options:
        'IMAP_flight': 
        'IMAP_finCal':
        'IMAP_preCal2':
        'IBEX_finCal':
        'IBEX_flight':
    '''
    from pandas import Series
    g_spokes = {
            'IMAP_flight':{
                            'coll_trans':1/.96,
                            'p10_trans':.91,
                            'tof_trans': .6,
                            'p2_trans': .89,
                            },
            'IMAP_finCal':{
                            'coll_grid':.92,
                            'p10_trans':.91,
                            'tof_trans': .6,
                            'p2_grid': 1,
                            },
            'IMAP_preCal2':{
                            'coll_grid':1,
                            'p10_trans':.91,
                            'tof_trans': .6,
                            'p2_grid': 1,
                            },
            'IBEX_finCal':{
                            'coll_grid':.92,
                            'coll_grnd_grid':.9,
                            'p2_grid': .855,
                            'p10_Trans':.83,
                            'tof_trans':.5504
                            },
            'IBEX_flight':{
                            'coll_grnd_grid':.9,
                            'p2_grid': .855,
                            'p10_Trans':.83,
                            'tof_trans':.5504
                            }
                
                }
    return(Series(g_spokes[instrument_config]))

def get_mcp_gain(species = 'H2'):
    '''
    import silver triple mcp gain curve function for a given species. 
    - MCP gain curves loaded from 20241218_T105_FinalCal_MCP_Gain.pkl. 
    - Gian curves generated from final cal data in 20241218_T105_FinalCal_MCP_Gain.ipynb
    
    Input:
        species [str]: calibration species for gain curve
        Options:
            'D/H2'
            'H2'
            'He'
            'O'
    Output:
        Jonda: cubic interpolation of averaged and smoothed gain curve measurements
    '''

    from pandas import read_pickle
    from os.path import dirname,join
    lpath = dirname(__file__)
    for up in range(2):
        lpath = dirname(lpath+'..')

    f_data = join(lpath,"cal/cal_results/20241218_T105_FinalCal_MCP_Gain.pkl")
    return(read_pickle(f_data)[species])


def get_inst_response(species = 'H'):
    '''
    import instrument energy response funciton calibcated from final cal. 
    - Response functions loaded from fin_cal1_H_KE_Response.pkl. 
    
    Input:
        species [str]: calibration species for gain curve
        Options:
            'D/H2'
            'H2'
            'He'
            'O'
    Output:
    '''

    from pandas import read_pickle
    from os.path import dirname,join
    lpath = dirname(__file__)
    for up in range(2):
        lpath = dirname(lpath+'..')

    f_data = join(lpath,"cal/cal_results/fin_cal1_H_KE_Response.pkl")
    return(read_pickle(f_data))